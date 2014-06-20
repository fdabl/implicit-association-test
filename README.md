# Implicit Association Test

The Implicit Association Test (IAT) is a measure of implicit cognition, see the original paper here:

Greenwald, A. G., McGhee, D. E., & Schwartz, J. L. (1998). Measuring individual differences in implicit cognition:
the implicit association test. *Journal of personality and social psychology, 74*(6), 1464.

Following Nosek, B. A., Greenwald, A. G., & Banaji, M. R. (2005), the assignment to one of the two different trial orders is randomized and the fifth block always
contains 40 instead of 20 trials.

Greenwald, A. G., Nosek, B. A., & Banaji, M. R. (2003) discuss an improved scoring algorithm. I will implement this when
I can find some spare time.

This code implements the IAT in a clean and modular fashion. More specifically, it is a self-other variant of the IAT.
The stimuli words are from Greenwald, A. G., & Farnham, S. D. (2000).

However, you can configure it to match your specific IAT type by changing the stimuli.csv file and the variables
allRes (line 31) and pos, neg, self, other (line 36). In the main function, you can add your specific instructions beneath each block.

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

You are welcome to use this code for personal or academic uses. If you fork, or use this in an academic paper please cite as follows:

Dablander, F. (2014). Implicit Association Test in Python (Version 1.00)[Software]. Available from [https://github.com/dostodabsi/implicit-association-test](https://github.com/dostodabsi/implicit-association-test).


# Note
The code was originally written for the bachelor thesis of my dear colleague Gabriela Hofer ([@gabriela_hofer](https://twitter.com/gabriela_hofer)). She
read up on the whole literature and gave me detailed instructions on the IAT.

# LICENCE
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
