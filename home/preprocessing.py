import pandas as pd
import numpy as np
import math

df = pd.read_csv(".\\.\\total 3.csv" , encoding='cp949')

def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # 유클리드 거리 계산
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance

def find_closest_coordinates(base_coord, coordinates, num_closest):
    # 주어진 기준 좌표를 제외한 좌표 리스트 생성
    filtered_coords = [coord for coord in coordinates if coord != base_coord]

    # 기준 좌표와 각 좌표 사이의 거리를 계산합니다.
    distances = [(coord, calculate_distance(base_coord, coord)) for coord in filtered_coords]

    # 거리를 기준으로 가장 가까운 순서대로 정렬합니다.
    sorted_distances = sorted(distances, key=lambda x: x[1])

    # 가장 가까운 세 좌표를 선택합니다.
    closest_coordinates = [coord for coord, _ in sorted_distances[:num_closest]]

    return closest_coordinates

def calculate_distance_ratio(coordA, coordB, coordC):
    # A와 B 사이의 거리 계산
    distance_AB = calculate_distance(coordA, coordB)

    # A와 C 사이의 거리 계산
    distance_AC = calculate_distance(coordA, coordC)

    # B와 C 사이의 거리 계산
    distance_BC = calculate_distance(coordB, coordC)

    # 거리 비율 계산
    if distance_AC == 0:
        ratio_AB_AC = 1
        ratio_BC_AC = 1
    else:
        ratio_AB_AC = distance_AB / distance_AC
        ratio_BC_AC = distance_BC / distance_AC

    return ratio_AB_AC, ratio_BC_AC

def weighted_average(data):
    total_weight = 0
    weighted_sum = 0

    # 가중 평균을 계산하기 위해 데이터를 반복합니다.
    for value, weight in data:
        # 가중치를 곱하여 가중합을 계산합니다.
        value = float(value)
        weighted_sum += value * weight

        # 가중치의 총합을 계산합니다.
        total_weight += weight

    # 가중 평균 값을 계산합니다.
    weighted_avg = weighted_sum / total_weight

    return weighted_avg

def calculate_weighted_average(base_coordinate, houseType):
    df = pd.read_csv(".\\.\\total 3.csv" , encoding='cp949')

    # 데이터 프레임으로부터 필요한 데이터를 추출합니다.
    data1 = df[df["매물 구분"].str.contains("전세")].reset_index(drop=True)
    data2 = df[df["매물 구분"].str.contains("월세")].reset_index(drop=True)
    data3 = df[df["매물 구분"].str.contains("매매")].reset_index(drop=True)

    data1_coordinate = data1[['위도', '경도']]
    data1_price = data1['보증금']

    data2_coordinate = data2[['위도', '경도']]
    data2_price = data2['보증금']
    data2_rent = data2['월세 금액']

    data3_coordinate = data3[['위도', '경도']]
    data3_price = data3['매매 금액']

    # 좌표, 값 리스트를 선택합니다.
    if houseType == '전세':
        coordinate_list = data1_coordinate.values.tolist()
        price_list = data1_price.tolist()
        result = calculate_weighted_average_helper(base_coordinate, coordinate_list, price_list)
        return result
    elif houseType == '월세':
        coordinate_list = data2_coordinate.values.tolist()
        price_list = data2_price.tolist()
        price_list2 = data2_rent.tolist()
        result = calculate_weighted_average_helper(base_coordinate, coordinate_list, price_list)
        result2 = calculate_weighted_average_helper(base_coordinate, coordinate_list, price_list2)
        return result, result2
    elif houseType == '매매':
        coordinate_list = data3_coordinate.values.tolist()
        price_list = data3_price.tolist()
        result = calculate_weighted_average_helper(base_coordinate, coordinate_list, price_list)
        return result
    else:
        print("기준 좌표가 유효하지 않습니다.")
        return False

def calculate_weighted_average_helper(base_coordinate, coordinate_list, price_list):
    # 가장 가까운 세 좌표를 찾습니다.
    num_closest = 3
    closest_coordinates = find_closest_coordinates(base_coordinate, coordinate_list, num_closest)

    # 가장 가까운 세 좌표의 값을 가져옵니다.
    closest_values = [price_list[coordinate_list.index(coord)] for coord in closest_coordinates]

    print(closest_values)

    # 가장 가까운 세 좌표 사이의 거리 비율을 계산합니다.
    ratio_AB_AC, ratio_BC_AC = calculate_distance_ratio(closest_coordinates[0], closest_coordinates[1], closest_coordinates[2])

    # 가중 평균을 계산하기 위한 (값, 가중치) 쌍의 리스트를 생성합니다.
    data = [(value, ratio_AB_AC) for value in closest_values] + [(value, ratio_BC_AC) for value in closest_values] + [(value, 1) for value in closest_values]

    print(data)

    # 가중 평균을 계산합니다.
    result = weighted_average(data)

    return result
 