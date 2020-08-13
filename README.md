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
Name              Min  FG     3PT  FT     OREB  DREB  REB  AST  STL  BLK  TO  PF  PTS  +/-  
Todd Marshack     21   3-7    0-1  1-1    1     0     1    5    1    0    5   2   7    -4   
Isaac Paben       28   3-8    1-2  1-1    2     3     5    3    2    0    1   4   8    4    
Jermaine Hanson   19   4-7    0-1  0-0    0     5     5    2    0    1    0   5   8    1    
Marcus Neely      29   6-10   0-1  1-2    2     7     9    4    0    3    2   4   13   -6   
Kwame Williams    26   5-7    0-0  3-4    0     4     4    2    1    1    1   2   13   6    
Paul Lilly        27   5-9    2-3  2-4    1     2     3    3    0    1    5   2   14   0    
Erik Green        19   3-5    1-1  2-2    1     2     3    1    0    1    2   4   9    13   
Bobby Jones       14   0-0    0-0  2-2    0     0     0    1    1    0    0   2   2    -8   
Jim Braxton       10   2-3    0-0  1-2    0     0     0    0    1    0    0   1   5    -3   
Michael Everhart  3    0-0    0-0  0-0    0     1     1    1    0    0    0   1   0    2    
Darren Tuck       1    0-0    0-0  0-0    0     0     0    0    0    0    0   0   0    0    
Ray Herbert       DNP  
Derek Smith       DNP  
Matt Prescott     DNP  
TEAM                   31-56  4-9  13-18  7     24    31   22   6    7    16  27  79        


Name              Min  FG     3PT   FT     OREB  DREB  REB  AST  STL  BLK  TO  PF  PTS  +/-  
Isaac Punt        26   2-6    1-3   1-4    1     2     3    6    0    1    3   2   6    0    
Tony Hedrick      31   5-9    1-4   5-5    0     2     2    2    3    1    2   1   16   4    
Kyle King         31   5-7    2-2   8-10   1     2     3    0    0    0    0   0   20   2    
Andrew Broderick  28   1-7    0-0   3-8    1     3     4    1    0    2    0   1   5    -5   
Corey Mitchell    27   4-10   0-1   4-4    1     5     6    1    0    1    1   3   12   -2   
Alan King         15   2-2    0-0   0-0    0     4     4    2    0    1    0   2   4    -7   
Michael Greer     12   3-4    0-0   3-4    0     1     1    0    0    0    0   2   9    1    
Rashod Branch     11   0-1    0-1   2-2    0     0     0    2    2    0    2   2   2    4    
Jason Ashman      8    0-0    0-0   2-2    1     0     1    0    2    0    0   1   2    -3   
Michael Lewis     7    1-2    0-1   0-0    0     0     0    0    1    0    1   2   2    1    
Lonnie Maxwell    DNP  
Landon Dixon      DNP  
Vic Shumpert      DNP  
Jason Crowley     DNP  
Mark Dench        DNP  
TEAM                   23-48  4-12  28-39  5     19    24   14   8    6    9   16  78                 
```
