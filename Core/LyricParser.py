# -*- coding: utf-8 -*-

__author__ = 'n1213 <myn1213@corp.netease.com>'

import os
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class LyricParser:
    @staticmethod
    def parse(lrc_path):
        if not os.path.exists(lrc_path):
            raise IOError(u'[ERROR] %s not exist.' % lrc_path)
        dict_lyric = dict()
        lrc_file = open(lrc_path, 'r')
        pattern = re.compile(r'\[\d{2}:\d{2}\.\d{2}\]')
        try:
            while True:
                str_line = lrc_file.readline().decode("utf-8")
                if len(str_line) == 0:
                    break
                last_timestamp = ''
                for m in pattern.finditer(str_line):
                    last_timestamp = m.group()
                lyric_text = str_line[str_line.index(last_timestamp) + len(last_timestamp):]
                for m in pattern.finditer(str_line):
                    timestamp = m.group()
                    time = long(timestamp[1:3]) * 60 * 1000 + long(timestamp[4:6]) * 1000
                    dict_lyric[time] = lyric_text
        except IOError:
            print(u'[ERROR] IO error, please check!')
            exit(1)
        except:
            print(u'[ERROR] Program exception!')
            exit(1)
        finally:
            lrc_file.close()
        return dict_lyric
