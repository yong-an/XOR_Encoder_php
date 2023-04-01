import argparse
import string
import random
import re

class Encoder():
    DEFAULT_CHARSET = string.ascii_letters + string.digits
    SEPARATORS = '()[]{}:;+-/ "' 

    def calXORChar(self, payload_char, charset=DEFAULT_CHARSET, randomize=True):
        for first_char in (charset if not randomize else "".join(random.sample(charset, len(charset)))):
            for second_char in (charset if not randomize else "".join(random.sample(charset, len(charset)))):
                third_char = chr(ord(first_char) ^ ord(second_char) ^ ord(payload_char))
                if third_char != payload_char and third_char in charset:
                    return [first_char, second_char, third_char]
        raise Exception("Charset not valid for this payload. char=%c charset=%s" % (payload_char, charset))

    def calXORString(self, payload, charset=DEFAULT_CHARSET, randomize=True):
        if payload[0] == '"':
            payload = payload[1:-1]
        result = ["", "", ""]
        for c in payload:
            xored_chars = self.calXORChar(c, charset=charset, randomize=randomize)
            for i in range(3):
                result[i] += xored_chars[i]

        return result

    def encode(self, payload, charset=DEFAULT_CHARSET, randomize=True, badchars=""):
        charset = "".join([x if x not in badchars else "" for x in charset])

        payload_array = re.split(r'(\"[\w\- ]+\")|([\w\.]+)', payload)
        result = ""
        for word in payload_array:
            if word == None: continue
            if word == "" or word in self.SEPARATORS:
                result += word
                continue

            xored_words = self.calXORString(word, charset=charset, randomize=randomize)
            xored_words = ['"' + x + '"' for x in xored_words]

            result += "(" + "^".join(xored_words) + ")"

        while True:
            match = re.search(r'(\(\([\^\w\"]+)\)\)', result)
            if not match: break
            result = result.replace(match.group(0), match.group(0)[1:-1])
        return result

def main():
    parser = argparse.ArgumentParser(description="Encoder for payloads")
    grouped = parser.add_mutually_exclusive_group(required=True)
    grouped.add_argument("--encode", "-e", help="Encode the payload")
    parser.add_argument("--number", "-n", default=1, type=int, help="Generate number of payload")
    groupcb = parser.add_mutually_exclusive_group()
    groupcb.add_argument("--charset", "-c", default=string.ascii_letters + string.digits,
                         help="Select specific charset for encoding")
    groupcb.add_argument("--badchars", "-b", default="", help="Select specific badchars for encoding")

    args = parser.parse_args()

    if args.encode is not None:
        try:
            for _ in range(args.number):
                result = Encoder().encode(args.encode, charset=args.charset, badchars=args.badchars)
                print(result)
        except Exception as ex:
            print("Error encoding the payload: ", ex)

if __name__ == "__main__":
    main()
