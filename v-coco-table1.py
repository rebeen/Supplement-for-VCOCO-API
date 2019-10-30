import vsrl_utils as vu
import numpy as np
import os
from pycocotools.coco import COCO


def get_aciton_num_and_roles_num(dataset_name='vcoco_trainval', action='sit'):
    coco = vu.load_coco()

    # Load the VCOCO annotations for vcoco_train image set
    vcoco_data = vu.load_vcoco(dataset_name)

    classes = [x['action_name'] for x in vcoco_data]
    cls_id = classes.index(action)

    vcoco = vcoco_data[cls_id]

    positive_index = np.where(vcoco['label'] == 1)[0]
    total = len(positive_index)
    # print("total", total)

    x1 = set()
    x2 = set()
    count1 = 0
    count2 = 0
    for i in range(1, len(vcoco['role_name'])):
        for j in range(vcoco_data[0]['ann_id'].shape[0]):
            if vcoco['role_object_id'][j][i] != 0:
                if i == 1:
                    # get anno id
                    x1.add(vcoco['role_object_id'][j][i])
                    count1 = count1 + 1
                else:
                    x2.add(vcoco['role_object_id'][j][i])
                    count2 = count2 + 1

    # print("count1", count1)
    # print("count2", count2)

    # get category_ids
    anns = coco.loadAnns(list(x1))
    category_ids = np.array([a['category_id'] for a in anns])
    category_ids_list1 = np.sort(list(set(category_ids)))

    anns = coco.loadAnns(list(x2))
    category_ids = np.array([a['category_id'] for a in anns])
    category_ids_list2 = np.sort(list(set(category_ids)))

    return [total, count1, count2, category_ids_list1, category_ids_list2, vcoco['role_name']]


def get_names(cats_list):
    # print(cats_list)
    coco = COCO(os.path.join('coco/annotations/', 'instances_trainval2014.json'))
    cates = coco.loadCats(list(cats_list))
    # print(cates)
    return np.array([a['name'] for a in cates])


def merge_two_list(list1, list2):
    list_all = set()
    for i in range(len(list1)):
        list_all.add(list1[i])
    for j in range(len(list2)):
        list_all.add(list2[j])
    return np.sort(list(list_all))


def get_table1_one_row(action='carry'):
    trainval_list = get_aciton_num_and_roles_num(dataset_name='vcoco_trainval', action=action)
    test_list = get_aciton_num_and_roles_num(dataset_name='vcoco_test', action=action)

    category_ids_list1 = merge_two_list(trainval_list[3], test_list[3])
    name_list1 = get_names(category_ids_list1)
    # print(name_list1)

    if trainval_list[2] != 0:
        category_ids_list2 = merge_two_list(trainval_list[4], test_list[4])
        name_list2 = get_names(category_ids_list2)
        # print(name_list2)

    print("1.Action:", action)
    print('2.Roles:', "1" if len(trainval_list[5]) == 2 else "2")
    print("3.numbers of example:", trainval_list[0] + test_list[0])

    for i in range(1, len(trainval_list[5])):
        print("4.", trainval_list[5][i])
        print("5.", trainval_list[1] + test_list[1] if i == 1 else trainval_list[2] + test_list[2])
        print("6.Objects in role:", name_list1 if i == 1 else name_list2)


if __name__ == '__main__':
    # get_table1_one_row(action='sit')
    get_table1_one_row(action='hit')
