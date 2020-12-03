import pandas as pd


def init_frame(config):
    fields = {
        "time": [] 
    }

    for i in range(1, 4):
        if config.get_pos:
            fields[f"x_{i}"] = []
            if config.dim > 1:
                fields[f"y_{i}"] = []
            if config.dim > 2:
                fields[f"z_{i}"] = []
        if config.get_speed:
            fields[f"vx_{i}"] = []
            if config.dim > 1:
                fields[f"vy_{i}"] = []
            if config.dim > 2:
                fields[f"vz_{i}"] = []
        if config.get_acc:
            fields[f"ax_{i}"] = []
            if config.dim > 1:
                fields[f"ay_{i}"] = []
            if config.dim > 2:
                fields[f"az_{i}"] = []
    
    return pd.DataFrame(fields)


def write_data(data_frame, config, system, i, t, acc):
    for i in range(3):
        if config.get_pos:
            data_frame.append({f"x_{i+1}": system.r[i][0]}, ignore_index=True)
            if config.dim > 1:
                data_frame.append({f"y_{i+1}": system.r[i][1]}, ignore_index=True)
            if config.dim > 2:
                data_frame.append({f"z_{i+1}": system.r[i][2]}, ignore_index=True)
        if config.get_speed:
            data_frame.append({f"vx_{i+1}": system.v[i][0]}, ignore_index=True)
            if config.dim > 1:
                data_frame.append({f"vy_{i+1}": system.v[i][1]}, ignore_index=True)
            if config.dim > 2:
                data_frame.append({f"vz_{i+1}": system.v[i][2]}, ignore_index=True)
        if config.get_acc:
            data_frame.append({f"ax_{i+1}": acc[i][0]}, ignore_index=True)
            if config.dim > 1:
                data_frame.append({f"ay_{i+1}": acc[i][1]}, ignore_index=True)
            if config.dim > 2:
                data_frame.append({f"az_{i+1}": acc[i][2]}, ignore_index=True)
    return data_frame