from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Common.config import *
from itsdangerous import BadSignature, SignatureExpired

def swap(l,index1,index2):
        '''
        swap the two given index element in the list and return the index2
        :param l:
        :param index1:
        :param index2:
        :return: index2
        '''
        l[index1],l[index2] = l[index2],l[index1]
        return index2

def bubble_down(drivers, index, length=None):
    '''
    helper function for the heap sort of drivers
    :param drivers:
    :param index:
    :return:
    '''
    if not length:
        length = len(drivers)
    left_child_index = index * 2 + 1
    right_child_index = index * 2 + 2
    if left_child_index < length:
        if right_child_index < length:
            if drivers[index].distance > drivers[left_child_index].distance \
                    or drivers[index].distance > drivers[right_child_index].distance:
                index = swap(drivers, index, left_child_index) \
                    if drivers[left_child_index].distance < drivers[right_child_index].distance \
                    else swap(drivers, index, right_child_index)
                bubble_down(drivers, index)
        else:
            if drivers[index].distance > drivers[left_child_index].distance:
                index = swap(drivers, index, left_child_index)
                bubble_down(drivers, index)

def find_zone(long,lati):
    '''
    find the zone where the driver is
    :param long:
    :param lati:
    :return: if the location is valid, return the corresponding zone otherwise return -1
    '''
    if long < 0 or lati < 0 or long > 90 or lati > 90:
        return -1
    return  (long)//10 + (lati)//10*10

def create_token(user_id,expiration=EXPIRATION):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    token_content = {}
    token_content["user_id"] = user_id
    return s.dumps(token_content)

def verify_token_and_return_data(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
        return data
    except SignatureExpired:
        print('token is expired')
        return None
    except BadSignature:
        return None
