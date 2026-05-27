import pandas as pd

def process_fuzzer_log_hybrid(input_file, output_file):
    df = pd.read_csv(input_file, skipinitialspace=True)
    
    if '# unix_time' in df.columns:
        df.rename(columns={'# unix_time': 'unix_time'}, inplace=True)
    elif 'unix_time' not in df.columns and df.columns[0].endswith('unix_time'):
        df.rename(columns={df.columns[0]: 'unix_time'}, inplace=True)

    t0 = df['unix_time'].iloc[0]
    df['minutes_run'] = (df['unix_time'] - t0) / 60.0

    if 'map_size' in df.columns and df['map_size'].dtype == object:
        df['map_size'] = df['map_size'].astype(str).str.rstrip('%').astype(float)

    targets = [60, 180, 360, 720]
    result_rows = []

    for target in targets:
        exact_matches = df[(df['minutes_run'] >= target) & (df['minutes_run'] < target + 1)]
        
        if not exact_matches.empty:
            row = exact_matches.iloc[0].copy()
            row['minutes_run'] = target  
            result_rows.append(row)
        else:
            before = df[df['minutes_run'] < target]
            after = df[df['minutes_run'] > target]
            
            if not before.empty and not after.empty:
                row_before = before.iloc[-1]
                row_after = after.iloc[0]
                
                t = target
                t1 = row_before['minutes_run']
                t2 = row_after['minutes_run']
                
                interp_row = pd.Series(dtype=float)
                
                for col in df.columns:
                    y1 = row_before[col]
                    y2 = row_after[col]
                    interp_row[col] = y1 + (t - t1) * (y2 - y1) / (t2 - t1)
                    
                interp_row['minutes_run'] = target
                result_rows.append(interp_row)
            else:
                print(f"Bỏ qua mốc {target} phút: Log chưa chạy tới thời điểm này.")

    if not result_rows:
        return

    res_df = pd.DataFrame(result_rows)

    int_cols = ['unix_time', 'cycles_done', 'cur_path', 'paths_total', 'pending_total', 
                'pending_favs', 'unique_crashes', 'unique_hangs', 'max_depth']
    for col in int_cols:
        if col in res_df.columns:
            res_df[col] = res_df[col].round().astype(int)

    if 'map_size' in res_df.columns:
        res_df['map_size'] = res_df['map_size'].round(2).astype(str) + '%'
    if 'execs_per_sec' in res_df.columns:
        res_df['execs_per_sec'] = res_df['execs_per_sec'].round(2)

    cols = res_df.columns.tolist()
    cols.remove('minutes_run')
    cols.insert(1, 'minutes_run')
    res_df = res_df[cols]

    res_df.to_csv(output_file, index=False)
    print(f"DONE: {output_file}")

process_fuzzer_log_hybrid('plot_data', 'formatted_plot_data.csv')