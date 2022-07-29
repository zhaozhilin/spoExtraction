import json
import os


class postprocess():
    def __init__(self):
        self.schema_path = 'raw_data/chinese/duie_schema.json'
        self.result_dev_path = 'result_dev1.json'

    def get_schema_dict(self):
        schema_dict = {}
        for line in open(self.schema_path, 'r'):
            spo = json.loads(line)
            predicate = spo['predicate']
            object_type = spo['object_type']
            subject_type = spo['subject_type']
            schema_dict[predicate] = [object_type, subject_type]
        return schema_dict

    def gen_result_one(self, schema_dict):
        load_f = open(self.result_dev_path, 'r')
        fwjson = open("result_post_process.json", 'w')
        #fwjson.write(json.dumps(result_dict, ensure_ascii=False) + '\n')
        for line in load_f:
            result_dict = {}
            load_result_dict = json.loads(line)
            text = load_result_dict['text']
            #result_dict['text'] = text
            spo_line = load_result_dict['spo_list']
            spo_line_list = []
            spo_formal_dict = {}
            if len(spo_line) != 0:
                for spo_one in spo_line:
                    predicate_ot = spo_one['predicate']
                    object = spo_one['object']
                    subject = spo_one['subject']
                    if subject == object:
                        continue
                    if '_' in predicate_ot:
                        predicate, ot = predicate_ot.split("_")
                        flag = 0
                        for id, spo in enumerate(spo_line_list):
                            if spo['predicate'] == predicate and spo['subject'] == subject:
                                flag = 1#如果已经出现过了 直接添加到后面  不然创建一个新的spolist
                                break
                        if flag == 0:
                            spo_formal_dict = {}
                            spo_formal_dict['predicate'] = predicate
                            spo_formal_dict['object_type'] = {}
                            spo_formal_dict['object_type'][ot] = schema_dict[predicate][0][ot]
                            spo_formal_dict['subject_type'] = schema_dict[predicate][1]#schema_dict里面的object_type的属性以及值

                            spo_formal_dict['object'] = {}
                            spo_formal_dict['object'][ot] = object
                            spo_formal_dict['subject'] = subject
                            spo_line_list.append(spo_formal_dict)
                        else:
                            spo_formal_dict['object_type'][ot] = schema_dict[predicate][0][ot]
                            spo_formal_dict['object'][ot] = object

                    else:
                        spo_formal_dict = {}
                        predicate = predicate_ot
                        spo_formal_dict['predicate'] = predicate
                        spo_formal_dict['object_type'] = schema_dict[predicate][0]#schema_dict里面的object_type的属性以及值
                        spo_formal_dict['subject_type'] = schema_dict[predicate][1]#schema_dict里面的subject_type的属性以及值
                        spo_formal_dict['object'] = {}
                        spo_formal_dict['object']['@value'] = object
                        spo_formal_dict['subject'] = subject
                        spo_line_list.append(spo_formal_dict)


            '''if spo_line_list == []:
                spo_line_list.append({"predicate": " ", "object_type": {"@value": " "}, "subject_type": " ", "object": {"@value": " "}, "subject": " "})
            '''
            novalue_idx = []
            for idx, spo_one in enumerate(spo_line_list):
                if '@value' not in spo_one['object']:
                    novalue_idx.append(idx)
            if len(novalue_idx) != 0:
                for x in reversed(novalue_idx):
                    spo_line_list.pop(x)
            result_dict['spo_list'] = spo_line_list
            print(result_dict)
            fwjson.write(json.dumps(result_dict, ensure_ascii=False, indent= 4) + '\n')

'''
            if len(object_type) > 1:
                for key in object_type:
                    relation.append(predicate + '_' + key)
            else:
                relation.append(predicate)
            for r in relation:
                if r not in relation_vocab:
                    relation_vocab[r] = i
                    i += 1
        json.dump(relation_vocab,
                  open(self.relation_vocab_path, 'w'),
                  ensure_ascii=False)
'''
if __name__ == '__main__':
    postprocess = postprocess()
    schema_dict = postprocess.get_schema_dict()
    X = postprocess.gen_result_one(schema_dict)