import os
import random
import string

digits = string.hexdigits[:-6]
name = '0x' + ''.join(random.choice(digits) for _ in range(16))
print(name)
os.system('echo | set /p x="%s" | clip' % name)
