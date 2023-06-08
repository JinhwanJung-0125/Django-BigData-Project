import requests
import json
import pandas as pd
import time


url = 'https://apis.zigbang.com/v2/items/{}?domain=zigbang&version='  #������ ����, ���� ������ �⺻ api
ownerSeachUrl = 'https://apis.zigbang.com/v2/agents/{}?service_type=����' #������ �����߰�� ���� api
geohash = 'https://apis.zigbang.com/v2/items?domain=zigbang&geohash={}&needHasNoFiltered=true&new_villa=true&sales_type_in={}&zoom=15'  #������ geohash ��ġ�� ���� �Ź� ���� api 
seoulEastGeohash = ['wydm3', 'wydjz', 'wydq0', 'wydmb', 'wydm8', 'wydmc', 'wydm9' 'wydq6']    #�뷫 ���� ���� ���� geohash ��

def getListFromGeohash(location, sales_type):   #geohash ��ġ�κ��� item id list ������
    geohashUrl = geohash.format(location, sales_type)

    req = requests.get(geohashUrl)

    if req.status_code == 200:
        try:
            result = req.json()
            return result
        except json.JSONDecodeError as jsonError:
            print(jsonError)
            return False
    else:
        print('List�� �������� ����!\n')
        return False

def searchURL(itemID):  #api�� �Ź� ã��

    searchUrl = url.format(str(itemID))

    req = requests.get(searchUrl)

    if req.status_code == 200:
        try:
            result = req.json()
            return result
        except json.JSONDecodeError as jsonError:
            print(jsonError)
            return False
    else:
        print("item id�� �ش��ϴ� �Ź��� ����!\n")
        return False

def searchOwnerID(userID):  #api�� �����߰�� ����ڵ�Ϲ�ȣ ã��
    searchUrl = ownerSeachUrl.format(str(userID))

    req = requests.get(searchUrl)

    if req.status_code == 200:
        try:
            result = req.json()
            return result
        except json.JSONDecodeError as jsonError:
            print(jsonError)
            return False
    else:
        print('�����߰�� ���� Ž�� ����!\n')
        return False

 
def get_location(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": "KakaoAK 26e3dde9f6813271772df84583c77018"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    return api_json


count = 0   #���������� ã�� �Ź� ����
house_info = [] #���������� ã�� �Ź����� ����


for geohash_value in seoulEastGeohash:
    for salesType in ['����', '����', '�Ÿ�']:
        geohash_list = getListFromGeohash(geohash_value, salesType)
        items = geohash_list['items']

        for item in items:
            itemID = item['item_id']
            result = searchURL(itemID)

            if result != False: #�Ź��� ���������� ã�Ҵٸ� �ʿ��� ���� �̾Ƴ���
                if result['item']['jibunAddress'] == None:  #������ ���� ���
                    address = result['item']['addressOrigin']['local1'] + ' ' + result['item']['addressOrigin']['local2']   #���ּ�
                    jibunAddress = None #����
                    addressForMap = str(result['item']['addressOrigin']['local1'])
                    
                else:   #������ �ִ� ���
                    address = result['item']['addressOrigin']['local1'] + ' ' + result['item']['addressOrigin']['local2']   #���ּ�
                    jibunAddress = result['item']['jibunAddress']  #����
                    addressForMap = str(result['item']['addressOrigin']['local1'])+ ' ' + str(result['item']['jibunAddress'])
                
                locationResult = get_location(addressForMap)
                print(addressForMap)
                longitude = locationResult['documents'][0]['x']
                latitude = locationResult['documents'][0]['y']
                print(longitude, latitude)
                
                approve_date = result['item']['approve_date'] #�ذ��㰡 ��¥
                sales_type = result['item']['sales_type']   #�Ź� ����, ����, �Ÿ� ����
                floor = result['item']['floor'] + '��' #��
                guarentee = str(result['item']['�����ݾ�'])  #������
                monthly_price = str(result['item']['�����ݾ�'])  #������
                sales_price = str(result['item']['�Ÿűݾ�'])    #�Ÿű�
                updated_at = result['item']['updated_at']   #�Ź��� ���� �ֱ� ������Ʈ ��¥
                status_at = result['item']['����Ȯ��At']    #�Ź��� ���� ���� ��� ��¥
                suggest_item = result['tags'] #���� ��õ �Ź�
        
                user_no = result['item']['user_no'] #�����߰�� ���� id
                owner_info = searchOwnerID(user_no) #�����߰�� ���� ã��

                if owner_info != False: #�����߰�� ������ ���������� ã�Ҵٸ� �ʿ��� ���� �̾Ƴ���
                    agent_name = owner_info['agent_name']   #�����߰�� ���
                    agent_address = owner_info['address']   #�����߰�� �ּ�
                    agent_regid = owner_info['agent_regid'] #�����߰���� ����ڵ�Ϲ�ȣ

                    house_info.append([address] + [jibunAddress] + [approve_date] + [sales_type] + [floor] + [guarentee] + [monthly_price] + [sales_price]
                                        + [updated_at] + [status_at] + [suggest_item] + [agent_name] + [agent_address] + [agent_regid] + [latitude] + [longitude])

                else:   #�����߰�� ������ �� ã�Ҵٸ� �����߰�� ���� �κ��� None���� ó��
                    house_info.append([address] + [jibunAddress] + [approve_date] + [sales_type] + [floor] + [guarentee] + [monthly_price] + [sales_price]
                                        + [updated_at] + [status_at] + [suggest_item] + [None] + [None] + [None] + [latitude] + [longitude])

                count += 1



print('ã�� �� �Ź� ��: ', count)

zigBangHouseInfo_tbl = pd.DataFrame(house_info, columns = ('�� �ּ�', '����', '�ذ� �㰡 ��¥', '�Ź� ����', '�� ��ġ', '������', '���� �ݾ�', '�Ÿ� �ݾ�', 
                                                           '�ֱ� ������Ʈ ��¥', '���� ��� ��¥', '��õ �Ź� ����', '�����߰��', 
                                                           '�����߰�� �ּ�', '�����߰�� ����� ��� ��ȣ', '����' , '�浵'))

zigBangHouseInfo_tbl.to_csv('./�Ź� ����(�����浵 ����)_��������1.csv', encoding = 'cp949', mode = 'w', index = True)