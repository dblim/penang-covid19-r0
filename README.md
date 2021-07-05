# The Basic Reproductive Number of COVID-19 in Penang, Malaysia

This is a simple program to calculate the R_0 of COVID-19 for each of the 5 districts in Penang, Malaysia. Namely, Timur Laut, Barat Daya, Seberang Perai Utara, Seberang Perai Tengah and Seberang Perai Selatan. The code is written in a way that makes it easy to use for any other state in Malaysia. If you have ``python3`` with some basic packages installed (e.g. ``NumPy``), it is easy to modify the program for any state in Malaysia (see [Usage](#usage) below). In due time, we will attach an overleaf link for a detailed decription of how R_0 is calculated.


<p align="center">
  <img src="r0_vs_newcases.gif " alt="animated" width="50%">
</p>
<div style="margin:auto; width:80%">
  <p align="center">
  The evolution of R_0 vs daily cases per 100000 people for each district (TL, BD, SPU, SPT, SPS) in Penang, Malaysia. Notice towards the end of May/early June how
  the dots shift from green to yellow/red. This coincides with the spike in COVID-19 across Malaysia during the holiday
  season. GIF produced from R_0 values computed using [r0_model.py](https://github.com/dblim/penang-covid19/blob/main/r0_model.py).
  </p>
</div>

## Acknowledgements
I am grateful to [Eric Cooper](https://www.stanfordesp.org/teach/teachers/escooper/bio.html) for many insightful conversations on COVID-19. I would also like to thank [Kartik Chandra](https://cs.stanford.edu/~kach/) for his help with Git.

## COVID-19 Data 
The facebook page [Penang Lawan COVID-19](https://www.facebook.com/penanglawancovid19/) publishes daily reports of COVID-19 cases in Penang by district. I entered data from *loc. cit.* by hand into an excel file and used this as my dataset for Penang.

## Usage
To see a list of all optional command line arguments, as well as a description of what these arguments mean, do:

```
python3 r0_model.py --h
```

### Basic use


```
python3 r0_model.py input_dir input_file output_dir output_file
```


### Parameters 
The file ```params.py``` contains several parameters that you may modify for your own needs. If you want to use this for another state in Malaysia (e.g. Selangor), change ```REGION``` to your state and ```SUBREGIONS``` to the list of districts for that state.

## How you can help
Generally speaking, it is incredibly difficult to obtain COVID-19 data in Malaysia. The government publishes daily reports of COVID-19 statistics such as new cases, deaths and test positivity rates. However, to my knowledge there is no public repository of data stored in a systematic way in ``.xlsx`` or ``.csv`` files that are conducive to modelling. I would be more than happy if volunteers could help enter this data, in addition to other things such as daily deaths, test positivity rates, etc. If you wish to help, please email me.
