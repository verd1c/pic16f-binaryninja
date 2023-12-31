from enum import Enum

class RecordType(Enum):
    Data = 0
    EndOfFile = 1
    # These two are only used in INHX16
    # Extended Segment Address = 2
    # Start Segment Address = 3
    ExtendedLinearAddress = 4
    StartLinearAddress = 5

class Record():
    def __init__(self, line: bytes):
        self.parse(line)
    
    def parse(self, line: bytes):
        # Ignore all character preceding the first ':'
        start_code_idx = line.find(b':')
        if start_code_idx == -1:
            raise ValueError("Line does not contain valid start code")
        line = line[start_code_idx + 1:]
        self.byte_count = int(line[0:2], 16)
        self.address = int(line[2:6], 16)
        self.record_type = RecordType(int(line[6:8], 16))

        end_data = self.byte_count*2
        self.data = bytes.fromhex(line[8:8+end_data].decode('ascii'))
        self.checksum = line[8+end_data:10+end_data]
