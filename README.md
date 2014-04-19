# Implicit Association Test
Implementation of the IAT in a clean and modular fashion.

You can configure it to match your specific IAT type by changing the
stimuli.csv file and the variables allRes (line 30) and pos, neg, self, other (line 35). 
In the main function, you can add your specific instructions beneath each block.

helpers.py contains functions that are experiment agnostic and can be
used generically. Some tweaking may be required. You can get only the helpers.py
with 

```
curl -O https://raw.github.com/dostodabsi/implicit-association-test/master/helpers.py
```

The guys at <a href="http://gureckislab.org/">gureckislab</a> try to establish a <a href="http://psiturk.org">platform</a>
where browser-based experiments can be shared among researchers. In the spirit of
open science, I'd love to see a similar platform emerge for desktop experiments written
in Python / PsychoPy. If you have any ideas, please drop me an email at <a href="mailto: dostodabsi@gmail.com">dostodabsi@gmail.com</a>
or contact me over Twitter at <a href="http://twitter.com/fdabl" target="_blank">@fdabl</a>

# LICENCE
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>
