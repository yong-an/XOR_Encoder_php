# XOR Encoder
## Using XOR to bypass filters by obfuscating payload.
#### Since the ^ is the XOR operator, we are actually just dealing with binary numbers
#### If only one bit in a binary number is 1, the XOR operator will return 1, otherwise it will return 0 (00 = 0, 01 = 1, 10 = 1, 11 = 0). 
#### When you use XOR on a char, you are using the ASCII values (integer) of the char.
&nbsp;

| Char     | ASCII      | Binary   
| -------- | ---------- | --------    |
| `P`      | 80         | `1010000`   |
| `o`      | 111        | `1101111`   |
| `?`      | 63         | `0111111`   |

### This is also why "P" ^ "o" = "?"
&nbsp;
```
python3 encoder.py -e echo $name
>>>
("7nv5"^"kdt6"^"9ijl")
```