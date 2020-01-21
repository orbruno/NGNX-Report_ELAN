# NGNX-Report_ELAN
Python script for creating a CSV report with unique ffmpeg downloads with the format ffmpeg.*.deb or ffmpeg.*.rpm

## Requirements
This script requires Python 3 and Pandas
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas
```bash
pip3 install pandas
```

## Functions
NGNX_filtering.convert_to_csv(\*.log)


>Function expects an *\*.log* file from an NGNX access log, it will create a CSV file as an output, the IP address from the original report will be MD5 enconded

NGNX_filtering.ng.filter_requests(\*.csv)



>Function expects the *\*.csv* created with NGNX_filtering.convert_to_csv(*.log)function. As an output will return another a CSV file with only the unique hosts that requested to download ffmpeg.*.deb or ffmpeg.*.rpm packages


## To run script
From terminal use:
```bash
python3 -c 'import NGNX_filtering as ng; ng.convert_to_csv(r"access.log")'
python3 -c 'import NGNX_filtering as ng; ng.filter_requests("log.csv")'
```


