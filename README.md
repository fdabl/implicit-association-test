# Implicit Association Test
Implementation of the IAT in a clean and modular fashion.

You can configure it to match your specific IAT type by changing the
stimuli.csv file and the variables allRes (line 30) and pos, neg, self, other (line 35). 
In the main function, you can add your specific instructions beneath each block.

helpers.py contains functions that are experiment agnostic and can be
used generically. Some tweaking may be required. You can get only the helpers.py
with 

```
curl https://raw.github.com/dostodabsi/implicit-association-test/master/helpers.py > helpers.py
```
or

```
wget -qO- https://raw.github.com/dostodabsi/implicit-association-test/master/helpers.py > helpers.py
```

The guys at <a href="http://gureckislab.org/">gureckislab</a> try to establish a <a href="http://psiturk.org">platform</a>
where browser-based experiments can be shared among researchers. In the spirit of
open science, I'd love to see a similar platform emerge for desktop experiments written
in Python / PsychoPy. If you have any ideas, please drop me an email at <a href="mailto: dostodabsi@gmail.com">dostodabsi@gmail.com</a>
or contact me over Twitter at <a href="http://twitter.com/fdabl" target="_blank">@fdabl</a>

# Licence
The MIT License (MIT)

Copyright (c) 2014 Fabian Dablander

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
