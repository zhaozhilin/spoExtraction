import os
import json

from collections import Counter
from typing import Dict, List, Tuple, Set, Optional


class Chinese_selection_preprocessing(object):
    def __init__(self):
        self.raw_data_root = 'raw_data'
        self.data_root = 'duie'
        self.schema_path = os.path.join(self.raw_data_root, 'duie_schema.json')
        self.train = 'train_data.json'
        self.dev = 'dev_data.json'
        self.max_len = 512
        #self.test = os.path.join(self.raw_data_root, 'train_data.json')

        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(
                'schema file not found, please check your downloaded data!')
        if not os.path.exists(self.data_root):
            os.makedirs(self.data_root)

        self.relation_vocab_path = os.path.join(self.data_root,
                                                'relation_vocab.json')

    def relation_vocab(self):
        if os.path.exists(self.relation_vocab_path):
            pass
        else:
            self.gen_relation_vocab()
        return json.load(open(self.relation_vocab_path, 'r'))

    def gen_relation_vocab(self):
        relation_id_vocab = {}
        id_relation_vocab = {}
        i = 0
        for line in open(self.schema_path, 'r'):
            spo = json.loads(line)
            predicate = spo['predicate']
            object_type = spo['object_type']
            relation = []
            if len(object_type) > 1:
                for key in object_type:
                    relation.append(predicate + '_' + key)
            else:
                relation.append(predicate)
            for r in relation:
                if r not in relation_id_vocab:
                    relation_id_vocab[r] = i
                    i += 1

        i = 0
        for line in open(self.schema_path, 'r'):
            spo = json.loads(line)
            predicate = spo['predicate']
            object_type = spo['object_type']
            relation = []
            if len(object_type) > 1:
                for key in object_type:
                    relation.append(predicate + '_' + key)
            else:
                relation.append(predicate)
            for r in relation:
                if r not in id_relation_vocab:
                    id_relation_vocab[i] = r
                    i += 1
        all_relation = []
        all_relation.append(id_relation_vocab)
        all_relation.append(relation_id_vocab)
        json.dump(all_relation,
                  open(self.relation_vocab_path, 'w'),
                  ensure_ascii=False, indent= 4)

    def gen_vocab(self, min_freq: int):
        source = os.path.join(self.raw_data_root, self.train)
        target = os.path.join(self.data_root, 'word_vocab.json')
        target1 = os.path.join(self.data_root, 'word_vocab.txt')

        cnt = Counter()  # 8180 total
        fw = open(target1, "a")
        with open(source, 'r') as s:
            for line in s:
                line = line.strip("\n")
                if not line:
                    return None
                instance = json.loads(line)
                text = list(instance['text'])
                cnt.update(text)
        result = {'[PAD]': 0}
        i = 1
        for k, v in cnt.items():
            if v > min_freq:
                result[k] = i
                i += 1
        result['oov'] = i
        for w in result:
            fw.write(w)
            fw.write("\n")
        json.dump(result, open(target, 'w'), ensure_ascii=False)

    def _read_line(self, line: str):
        line = line.strip("\n")
        if not line:
            return None
        instance = json.loads(line)
        text = instance['text']

        if 'spo_list' in instance:
            spo_list = instance['spo_list']

            if not self._check_valid(text, spo_list):
                return None
            spo_list1 = []
            for spo in spo_list:

                for key in spo['object']:
                    if spo['predicate'] in ['上映时间', '票房', '配音', '获奖', '饰演']:
                        predicate = spo['predicate'] + '_' + key
                    else:
                        predicate = spo['predicate']
                    object = spo['object'][key]
                    spo_dict = [
                                spo['subject'],
                                predicate,
                                object,
                                ]
                    spo_list1.append(spo_dict)

        result = {
            'text': text,
            'triple_list': spo_list1,
        }
        return result


    def _gen_one_data(self, dataset):
        source = os.path.join(self.raw_data_root, dataset)
        target = os.path.join(self.data_root, dataset)
        with open(source, 'r') as s, open(target, 'w') as t:
            result_all = []
            for line in s:
                newline = self._read_line(line)
                if newline != None:
                    result_all.append(newline)
            t.write(json.dumps(result_all, ensure_ascii=False, indent=4))

    def gen_all_data(self):
        self._gen_one_data(self.train)
        self._gen_one_data(self.dev)

    def _check_valid(self, text: str, spo_list: List[Dict[str, str]]) -> bool:
        if spo_list == []:
            return False
        #if len(text) > self.max_len:
        #    return False
        for t in spo_list:
            if t['subject'] not in text:
                return False
            for v in t['object']:
                if t['object'][v] not in text:
                    return False
        return True

    def spo_to_entities(self, text: str,
                        spo_list: List[Dict[str, str]]) -> List[str]:
        entities = set(t['subject'] for t in spo_list) | set(t['object'] for t in spo_list)
        return list(entities)

    def spo_to_relations(self, text: str,
                         spo_list: List[Dict[str, str]]) -> List[str]:
        return [t['predicate'] for t in spo_list]



if __name__ == '__main__':
    preprocessor = Chinese_selection_preprocessing()
    preprocessor.gen_relation_vocab()
    preprocessor.gen_all_data()
    preprocessor.gen_vocab(min_freq=1)
