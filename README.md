# DDS2020-College-Basketball-Box-Score-Generator
A python script that generates formatted box scores from Draft Day Sports College Basketball 2020 saved game data.

## How to use it
`c:\Users\chris\AppData\Local\Programs\Python\Python38-32\python.exe dds_game_log.py -f "C:\Program Files (x86)\Steam\steamapps\common\Draft Day Sports College Basketball 2020\app\disk\saves\backups\LongWood\LongWood.cbb" -to C:\Users\chris\Desktop -t Longwood "Wake Forest"`

Following `-t` should be the two teams that played in the game for which you want the box score
Following `-f` should be a path to the .cbb saved game file
Following `-to` should be a path to a directory where the box score file will be created.

* Important note that on Windows filepaths with spaces need to be enclosed in quotations. Likewise team names with spaces, like "Wake Forest" need to be enclosed in quotations.

## Nice Features
1) The box score is sorted to place starters first by position (PG, SG, SF, PF, C) then bench players sorted by minutes played. Those who didn't play get a "DNP" for their stat row.
2) The code pretty prints the box score so the spacing will always be right. You can adjust padding between columns by changing the `field_padding` parameter on the PrettyPrinter object.

## Ideas for improvement
1) Also generate csv so that these can be exported to excel, which could make for some cool statistical analyses. It shouldn't be too hard to do that with how the code is architected. The code is split into different sections - the first half parses the saved game file and creates player objects for each player. Then we pass these player objects into different `PlayerAnalyzer` objects. Currently we have three - one is untested: a `TotalTracker` which keeps track of the team totals as we iterate over each player, a `FileWriter` which writes output to a file, and a `ConsoleWriter` (untested) which should write output to the console. The `FileWriter` and `ConsoleWriter` both take a `Printer`, in this case the `PrettyPrinter` class that does all of the formatting. To generate csv we should only need to create a `CSVPrinter` class to format the data in csv style, and we should be able to reuse the `FileWriter` and `ConsoleWriter` objects.

2) Add team names to the box scores.

3) Add a way to request only certain stat lines

4) (this would require some pretty major work) Add a way to get cumulative team stats for the whole year

An example of a generated box score: 
```
         Name            Min       FG        3PT       FT        OREB      DREB      REB      AST      STL      BLK      TO      PF      PTS      +/-   
    Todd Marshack        27        2-7       0-1       4-4        0         6         6        4        1        2       2       1        8        9    
     Isaac Paben         21        4-5       0-1       0-0        0         3         3        4        2        0       3       2        8        8    
   Jermaine Hanson       26        2-4       0-1       1-2        1         1         2        1        1        0       0       2        5       10    
     Marcus Neely        21        5-9       0-1       1-3        1         1         2        1        1        2       1       2       11        6    
    Kwame Williams       21        3-8       0-0       6-7        2         5         7        3        3        3       0       0       12       14    
      Erik Green         18        1-2       0-0       5-6        0         5         5        1        0        0       1       2        7        5    
      Paul Lilly         16        3-4       1-1       0-2        0         1         1        2        1        0       2       0        7        6    
   Michael Everhart      14        2-7       1-3       2-2        0         2         2        0        1        0       3       3        7       -1    
     Jim Braxton         13        0-3       0-0       0-0        0         2         2        0        0        1       1       2        0       -7    
     Bobby Jones         13        2-3       0-0       2-2        1         3         4        1        1        0       0       0        6        1    
     Darren Tuck          4        0-0       0-0       0-0        0         0         0        0        0        0       1       0        0        4    
     Ray Herbert         DNP   
     Derek Smith         DNP   
    Matt Prescott        DNP   
         TEAM                     24-52      2-8      21-28       5         29       34       17       11        8       14      14      71             


       Name           Min       FG        3PT        FT        OREB      DREB      REB      AST      STL      BLK      TO      PF      PTS      +/-   
   Jeremy Watson      29        2-4       1-3        0-0        0         2         2        2        0        0       5       2        5       -17   
   Eddie Carroll      23        3-6       2-4        3-4        0         2         2        3        2        0       0       4       11       -4    
    Mark Givens       27        4-7       2-4        2-2        1         6         7        3        0        0       2       2       12       -6    
   Kevin Bartow       31        3-5       0-0        3-6        0         5         5        1        0        0       2       3        9       -14   
   Jeremy Allen       29       5-13       0-0        2-3        2         5         7        1        0        0       1       2       12       -7    
   Joey Thompson      19        1-6       1-5        3-4        0         1         1        0        0        0       2       1        6       -4    
   Carl Daniels       13        0-4       0-0        0-0        1         1         2        2        0        1       5       1        0       -4    
   Rickie Marek       13        0-1       0-1        3-4        0         2         2        0        1        0       0       1        3       -2    
   Herbert Lloyd      11        1-3       0-0        0-0        0         1         1        0        0        1       0       2        2        0    
   Solomon Leath       1        0-0       0-0        0-0        0         0         0        0        0        0       0       1        0        3    
    Cary Burris       DNP   
    Josh Floyd        DNP   
    Damous King       DNP   
   Daniel Langhi      DNP   
       TEAM                    19-49      6-17      16-23       4         25       29       12        3        2       17      19      60          
```
