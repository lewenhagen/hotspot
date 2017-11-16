def get_neigbours_inbound(data, rows, cols, distance, w, n_rows, r_len):
    """
    Calculates the neighbourhood, inbound
    """
    row_len, num_rows = data.shape
    m_sum = 0
    square_weight = 0
    j_count = 0

    min_x = 0 if (cols - distance) < 0 else (cols - distance)
    max_x = row_len if (cols + distance) > row_len else (cols + distance)

    min_y = 0 if (rows - distance) < 0 else (rows - distance)
    max_y = num_rows if (rows + distance) > num_rows else (rows + distance)

    if max_y < row_len and max_y > 0:
        max_y += 1

    if max_x < num_rows and max_x > 0:
        max_x += 1

    for trow in range(min_y, max_y):
        m_sum += data[trow, min_x:max_x].sum()

        for tcol in range(min_x, max_x):
            square_weight += (w * w)

        j_count += (max_x - min_x)

    return {"sum": m_sum, "square_weight": square_weight, "j_count": j_count}





def get_standard_deviation(data):
    """
    Returns the standard deviation from given matrix
    """
    sd_sum = data.sum()                             # summera alla features i dataset
    sd_square = sd_sum**2                           # square av summan
    square_divide = sd_square / data.size           # dela square med antalet features i dataset
    total_square_sum = np.sum(np.square(data))      # += feat * feat (samma som nedan kommenterat)
    # for value in data.flatten():
    #     total_square_sum += value**2

    total_square_sum -= sd_square                   # dra av sd_square från totala square summan
    total_of_feats = data.size - 1                  # dra av 1 från totalt antal features

    variance = total_square_sum / total_of_feats    # dela totala square summan med antalet feats (-1)
    standard_deviation = np.sqrt(variance)          # roten ur variance = standars deviation
    # print(standard_deviation)
