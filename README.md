# Fuzzing Script

## Introduction

Kho này chứa các script Python cho quá trình fuzzing. 

## List 

- `format_plot_data.py`
  - Đọc file `plot_data`
  - Chuẩn hóa cột `# unix_time` thành `unix_time`
  - Tính cột `minutes_run` theo phút kể từ lần ghi đầu tiên
  - Nội suy giá trị cho các mốc 60, 180, 360, 720 phút khi không có dòng log chính xác
  - Xuất file `formatted_plot_data.csv`

- `add_minutes_col.py`
  - Đọc file `plot_data`
  - Thêm cột `minutes_run`
  - Xuất file `plot_data_with_minutes.csv`