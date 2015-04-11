class Parser(object):
    def __init__(self):
        self.crop = None
        self.pest = None
        self.harvest = None

    def parse(self, raw):
        splits = raw.split(',')

        if len(splits) == 1:
            self.crop = splits[0]
        if len(splits) == 2:
            self.crop = splits[0]
            self.pest = splits[1]
        if len(splits) == 3:
            self.crop = splits[0]
            self.pest = splits[1]
            self.harvest = splits[2]

        return self.build_result()

    def build_result(self):
        return {
            'crop': clean(self.crop),
            'pest': clean(self.pest),
            'harvest': clean(self.harvest),
        } 

def clean(attr):
    """Clean up the farm data, ensures that nothing is None"""
    if attr is None:
        return ''
    posn = attr.find(':') if attr else -1
    if posn >= 0:
        attr = attr[posn+1:]
    return attr.strip()
