# Whisper-VITS-Japanese

### 教程在这里：https://www.bilibili.com/video/BV19e4y167Dx/?spm_id_from=333.999.0.0 

这个项目将Google的Whisper项目作为VITS的数据处理器，通过修改Whisper项目的transcribe.py，生成音频对应的Srt文件(这里使用的是被删掉的PR，现在已经找不到那个PR，所以无法引用到原作者)，同时将Whisper只能读取少数音频文件的限制，放宽到可以遍历文件夹下的所有音频文件。Whisper可以输出Srt使得长音频的输入成为可能，用户不需要再把音频切割零碎，甚至不需要再转写长音频的文本。我们直接靠Whisper进行语音识别和数据准备，自动切片为短音频，自动生成抄本文件，然后送入VITS训练流程。考虑到长时间的音频干声更容易获取，VITS入门壁垒再次大大降低。

处理流程大致如下：Whisper识别后的Srt文件会被auto.py处理，处理过程参考了[tobiasrordorf/SRT-to-CSV-and-audio-split: Split long audio files based on subtitle-info in SRT File (Transcript saved in CSV) (github.com)](https://github.com/tobiasrordorf/SRT-to-CSV-and-audio-split).  音频文件首先被转换为22050Hz和16bits，然后同名Srt文件的时间戳和语音识别的抄本被转换为csv文件，Csv文件中带有音频各段区间的起始时间、结束时间，以及对应的抄本和音频文件路径，然后采用AudioSegment这个包按照起始时间和结束时间切分长音频，按照切片顺序生成带有后缀的音频文件，例如A_0.wav和A_1.wav等等。所有被切片的音频都会被存入slice_audio文件夹，然后filelists文件夹下会生成VITS需要的带有“路径|转写”的txt文件，后续的数据流程就可以直接接上VITS部分。

我现在用的VITS的cleaner和symbol是[CjangCjengh/vits: VITS implementation of Japanese, Chinese, Korean and Sanskrit (github.com)](https://github.com/CjangCjengh/vits)作为创世神时期最初始的那版，现在他的仓库更新了更多的cleaner和symbol，不过我是很念旧的人，而且我很怀念刚开始大家来到VITS的时候，所以我还是用着最初的那版。VITS主要有两个预处理，一个是monotonic align，另一个是preprocess.py，然后就可以开始train.py。所有的流程我都放进了whisper-vits-japanese.ipynb，只需要逐行点击就能运行，唯一需要用户自己改动的地方就是把我的音频zip路径，换成你自己的音频zip，其余部分均不用修改。最后我还加上了把模型和处理好的文件存入网盘，以及下次训练时恢复从网盘恢复上次最新的checkpoint的指令。
