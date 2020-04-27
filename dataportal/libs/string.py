
class String(object):
    @staticmethod
    def cutnews(str, start, length):
        if len(str) > length:
            mvalue = str[start: start+length]+' ...'
        else:
            mvalue = str

        return mvalue
