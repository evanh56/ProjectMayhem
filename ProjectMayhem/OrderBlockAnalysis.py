import csv

counter = 0
def countRows(counter, data_file): #Does check and lines of data gotten
    with open(data_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            counter += 1
        return counter

def AddOB(ob_dict, val):
    if val == 0:
        with open('OrderBlock_15m.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ob_dict['Date'], ob_dict['Open'], ob_dict['High'], ob_dict['Low'], ob_dict['Close'], ob_dict['Position']])
    else:
        with open('OrderBlock_1hr.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ob_dict['Date'], ob_dict['Open'], ob_dict['High'], ob_dict['Low'], ob_dict['Close'], ob_dict['Position']])

def check_prev(prev_row, loc): # Checks if previous candle is incl in OB
    if loc == 1:
        if prev_row['Open'] - prev_row['Close'] > 0:
            return True
        else:
            return False
    if loc == 0:
        if prev_row['Open'] - prev_row['Close'] < 0:
            return True
        else:
            return False

def Next_candle(next1: object, next2: object, loc: object) -> int | None: # Checks position of proceeding candles
    if loc == 1:
        if next1['Open'] - next1['Close'] < 0 and next2['Open'] - next2['Close'] < 0: #Both bullish
            return 1
        else:
            return 0
    if loc == 0:
        if next1['Open'] - next1['Close'] > 0 and next2['Open'] - next2['Close'] > 0: #Both bearish
            return 1
        else:
            return 0

def OB_check(OrderBlock, counter, pos, loc, data_file):
    """
    Validates an Order Block with two stages:

    Stage 1: containment (next ~6 candles).
    Stage 2: activation + invalidation.
      - Bearish OB: must break ABOVE open to activate, then invalidates if later breaks BELOW open.
      - Bullish OB: must break BELOW open to activate, then invalidates if later breaks ABOVE open.
    """
    df = data_file
    len_df = len(df)

    ob_open  = float(OrderBlock['Open'])
    ob_close = float(OrderBlock['Close'])

    # Stage 1: Containment
    lo_body = min(ob_open, ob_close)
    hi_body = max(ob_open, ob_close)
    end_contain = min(pos + 6, counter - 1, len_df - 1)

    for j in range(pos + 1, end_contain + 1):
        c = df.iloc[j]
        co, cc = float(c['Open']), float(c['Close'])
        if lo_body <= co <= hi_body and lo_body <= cc <= hi_body:
            if loc == 1 and co > cc:   # bearish inside bearish OB
                return False
            if loc == 0 and cc > co:   # bullish inside bullish OB
                return False

    # Stage 2: Activation + Invalidation
    end_idx = min(counter - 1, len_df - 1)

    if loc == 1:  # bearish OB
        activated = False
        for i in range(pos + 2, end_idx + 1):
            c = df.iloc[i]
            o, h, l, cl = map(float, [c['Open'], c['High'], c['Low'], c['Close']])

            if not activated:
                if h > ob_open or o > ob_open or cl > ob_open:
                    activated = True
                continue
            else:
                if l < ob_open or cl < ob_open or o < ob_open:
                    return False
        return activated  # must have been activated and never invalidated

    else:  # bullish OB
        activated = False
        for i in range(pos + 2, end_idx + 1):
            c = df.iloc[i]
            o, h, l, cl = map(float, [c['Open'], c['High'], c['Low'], c['Close']])

            if not activated:
                if l < ob_open or o < ob_open or cl < ob_open:
                    activated = True
                continue
            else:
                if h > ob_open or o > ob_open or cl > ob_open:
                    return False
        return activated  # must have been activated and never invalidated



def Analyse_Data(data_file, val):
    df = data_file
    counter1 = len(df)
    for i in range(counter1 - 3):
        Current_row = df.iloc[i]
        Next_row = df.iloc[i + 1]
        Reentry = df.iloc[i + 2]
        if Current_row['Open'] - Current_row['Close'] >= 0: # Bearish
            loc = 1
            next_pos = Next_candle(Next_row, Reentry, loc) # Test for next OB
            if next_pos == 1:
                prev_row = df.iloc[i-1]
                if check_prev(prev_row, loc): #Check prev if in OB

                    new_ob = {
                        'Date': prev_row['Date'],
                        'Open': float(prev_row['Open']),
                        'High': float(prev_row['High']),
                        'Low': float(Current_row['Low']),
                        'Close': float(Current_row['Close']),
                        'Position': "Bearish"
                    }
                    if OB_check(new_ob, counter1, i, loc, data_file):  # Checks if OB has been taken out
                        AddOB(new_ob, val)
                else:
                    if OB_check(Current_row, counter1, i, loc, data_file):  # Checks if OB has been taken out
                        current_row = {
                            'Date': Current_row['Date'],
                            'Open': float(Current_row['Open']),
                            'High': float(Current_row['High']),
                            'Low': float(Current_row['Low']),
                            'Close': float(Current_row['Close']),
                            'Position': "Bearish"
                        }
                        AddOB(current_row, val)

        if Current_row['Open'] - Current_row['Close'] < 0: # Bullish
            loc = 0
            next_pos = Next_candle(Next_row, Reentry, loc) # Test for next OB
            if next_pos == 1:
                prev_row = df.iloc[i-1]
                if check_prev(prev_row, loc): #Check prev if in OB
                    new_ob = {
                        'Date': prev_row['Date'],
                        'Open': float(prev_row['Open']),
                        'High': float(prev_row['High']),
                        'Low': float(Current_row['Low']),
                        'Close': float(Current_row['Close']),
                        'Position': "Bullish"
                    }
                    if OB_check(new_ob, counter1, i, loc, data_file):  # Checks if OB has been taken out
                        AddOB(new_ob, val)
                else:
                    if OB_check(Current_row, counter1, i, loc, data_file):  # Checks if OB has been taken out
                        current_row = {
                            'Date': Current_row['Date'],
                            'Open': float(Current_row['Open']),
                            'High': float(Current_row['High']),
                            'Low': float(Current_row['Low']),
                            'Close': float(Current_row['Close']),
                            'Position': "Bullish"
                        }
                        AddOB(current_row, val)
    return

def main(data_file, val):
    Analyse_Data(data_file, val)
    return