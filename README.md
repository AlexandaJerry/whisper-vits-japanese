# Whisper-VITS-Japanese

### 教程在这里：https://www.bilibili.com/video/BV19e4y167Dx/?spm_id_from=333.999.0.0 
###  2023.01.31 更新了spec.pt损坏后自动生成新spec.pt以增强从网盘恢复训练的容错率

这个项目将Google的Whisper项目作为VITS的数据处理器，通过修改Whisper项目的transcribe.py，生成音频对应的Srt文件(这里使用的是被删掉的PR，现在已经找不到那个PR，所以无法引用到原作者)，同时将Whisper只能读取少数音频文件的限制，放宽到可以遍历文件夹下的所有音频文件。Whisper可以输出Srt使得长音频的输入成为可能，用户不需要再把音频切割零碎，甚至不需要再转写长音频的文本。我们直接靠Whisper进行语音识别和数据准备，自动切片为短音频，自动生成抄本文件，然后送入VITS训练流程。考虑到长时间的音频干声更容易获取，VITS入门壁垒再次大大降低。

处理流程大致如下：Whisper识别后的Srt文件会被auto.py处理，处理过程参考了[tobiasrordorf/SRT-to-CSV-and-audio-split: Split long audio files based on subtitle-info in SRT File (Transcript saved in CSV) (github.com)](https://github.com/tobiasrordorf/SRT-to-CSV-and-audio-split).  音频文件首先被转换为22050Hz和16bits，然后同名Srt文件的时间戳和语音识别的抄本被转换为csv文件，Csv文件中带有音频各段区间的起始时间、结束时间，以及对应的抄本和音频文件路径，然后采用AudioSegment这个包按照起始时间和结束时间切分长音频，按照切片顺序生成带有后缀的音频文件，例如A_0.wav和A_1.wav等等。所有被切片的音频都会被存入slice_audio文件夹，然后filelists文件夹下会生成VITS需要的带有“路径|转写”的txt文件，后续的数据流程就可以直接接上VITS部分。

我现在用的VITS的cleaner和symbol是[CjangCjengh/vits: VITS implementation of Japanese, Chinese, Korean and Sanskrit (github.com)](https://github.com/CjangCjengh/vits)作为创世神时期最初始的那版，现在他的仓库更新了更多的cleaner和symbol，不过我是很念旧的人，而且我很怀念刚开始大家来到VITS的时候，所以我还是用着最初的那版。VITS主要有两个预处理，一个是monotonic align，另一个是preprocess.py，然后就可以开始train.py。所有的流程我都放进了whisper-vits-japanese.ipynb，只需要逐行点击就能运行，唯一需要用户自己改动的地方就是把我的音频zip路径，换成你自己的音频zip，其余部分均不用修改。最后我还加上了把模型和处理好的文件存入网盘，以及下次训练时恢复从网盘恢复上次最新的checkpoint的指令。

---

### 下方部分由[Mr47121836](https://github.com/Mr47121836)完成，我们在此表示感谢
### 此外特致谢[失迹](https://github.com/Mitr-yuzr)指出的Numpy版本和文本预处理问题

### 2023.02.02添加了auto_ms.py,ms.json文件，进行多人训练就要运行auto_ms.py

#### 前期处理：

只需要将音频文件格式命名为 speakerId_XXXX.wav 上传到audio文件夹，之后按照一般步骤运行，到了音频处理就运行auto_ms.py文件，会自动生成txt文件，格式为Path|speakerId|text。

注意：若你使用了auto_ms.py来生成txt，必须在Alignment and Text Conversion这步修改为代码：(因为在多人训练时的text_index不是1而是2)
```
python preprocess.py --text_index 2 --text_cleaners japanese_cleaners --filelists /content/whisper-vits-japanese/filelists/train_filelist.txt /content/whisper-vits-japanese/filelists/val_filelist.txt
```

#### 训练：

```
python train_ms.py -c configs/ms.json -m ms
```
#### 多人模型接口部分使用：
```
hps = utils.get_hparams_from_file("./configs/ms.json")

net_g = SynthesizerTrn(
    len(symbols),  
    hps.data.filter_length // 2 + 1,  
    hps.train.segment_size // hps.data.hop_length,  
    n_speakers=hps.data.n_speakers,  
    **hps.model).cuda()  
_ = net_g.eval()  

_ = utils.load_checkpoint("/root/autodl-tmp/logs/ms/G_29000.pth", net_g, None)

stn_tst = get_text("ごめんね優衣", hps)
with torch.no_grad():  
    x_tst = stn_tst.cuda().unsqueeze(0)  
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()  
    sid = torch.LongTensor([11]).cuda() //11指speakerId为11，如果有12个n_speaker,编号就从0-11  
    audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()  
ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))  
```
