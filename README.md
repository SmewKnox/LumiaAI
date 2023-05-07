# LumiaAI
An AI voice-assistant powered by GPT and Eleven Labs

*Disclaimer*
I am not an experienced programmer I've only taken a freshman engineering class so far,
and that basically consisted of making basic if branhces and iterating through lists.
I am sure this is spaghetti code so if you have any suggestions please let me know.

Check out my youtube channel to keep up with progress.
https://www.youtube.com/channel/UC7MwaYTS1cRffSRgAqcJKUQ
----------------------------------------------------------------------------------------

How to use:
You must have the program and the lumiamem.txt file in the same folder.
additionally you must install all the modules, when you see import (name) on the top of the program,
copy and paste that name followed by "pypi" into google. click on the first result click the copy icon and paste into your terminal. The module will then begin
to download. Do this for every module.

Once you run the program and the console says "listening...", say the wake word name (which you can change to your liking) followed by your command.
The speechrecognition library will then convert your speech to text, feed it to the language model, the output text of the llm will then be fed to elevenlabs
and the AI will respond with a tts voice. As you might imagine this causes some delay, however in my testing most of the delay tends to come from the speechrecog.
Try to not talk with short sentences or one word respones because this causes the llm to autocomplete what it thinks would've followed your short response.
Additionally keep in mind that the speech recognition can get stuck on listening if there's too much background noise so you might want to adjust the thresh
variable, or add a phrase_time_limit paramter to "voice = listener.listen(source, timeout=10)". That said I got the best results when I started using noise
cancelling software on my mic. I use nvidiabroadcast.

To add fluidity to conversations with the AI I coded it to where you only have to say the wake word the first time, the second loop won't require it. However,
if nothing is said in this second loop, then by the third loop you will have to say the wake word again.

The AI has a handful of tasks that it can do however keep in mind that some of them are more finnicky than others and are still a work in progress.

The lumiamem.txt file stores the conversation allowing for you to ask the AI followup questions because by default it is a goldfish. However this increases token usage.
When you tell the AI to stop it's program this file is automatically wiped. However if you want to stop the program without wiping the memory you have to manually stop
the program yourself.



Usage costs:
This AI is powered by both eleven labs and GPT as such your wallet is gonna cry from two sources.
However you can disable the elevenlabs voice and use a normal tts voice to elimate that costs.(look at program notation for how to do so)
The GPT costs can be managed also, you can lower the token limit and additionally change the model to something that costs less. However, as mentioned before the
memory file increases token usage the longer your conversation so it might be a good idea to periodically terminate the program.
