# DDS2020-College-Basketball-Box-Score-Generator
A python script that generates formatted box scores from Draft Day Sports College Basketball 2020 saved game data.

## How to use it
python dds_game_log.py -t Longwood Drexel -f C:\Program Files (x86)\Steam\steamapps\common\Draft Day Sports College Basketball 2020\app\disk\saves\backups\Longwood\Longwood.cbb -to C:\Users\chris\Desktop

Following `-t` should be the two teams that played in the game for which you want the box score
Following `-f` should be a path to the .cbb saved game file
Following `-to` should be a path to a directory where the box score file will be created.

An example of a generated box score: 
```
         Name            Min       FG        3PT       FT        OREB      DREB      REB      AST      STL      BLK      TO      PF      PTS      +/-   
    Kwame Williams       21        3-8       0-0       6-7        2         5         7        3        3        3       0       0       12       14    
     Marcus Neely        21        5-9       1-0       1-3        1         1         2        1        1        2       1       2       11        6    
   Jermaine Hanson       26        2-4       1-0       1-2        1         1         2        1        1        0       0       2        5       10    
     Isaac Paben         21        4-5       1-0       0-0        0         3         3        4        2        0       3       2        8        8    
    Todd Marshack        27        2-7       1-0       4-4        0         6         6        4        1        2       2       1        8        9    
      Erik Green         18        1-2       0-0       5-6        0         5         5        1        0        0       1       2        7        5    
      Paul Lilly         16        3-4       1-1       0-2        0         1         1        2        1        0       2       0        7        6    
   Michael Everhart      14        2-7       3-1       2-2        0         2         2        0        1        0       3       3        7       -1    
     Jim Braxton         13        0-3       0-0       0-0        0         2         2        0        0        1       1       2        0       -7    
     Bobby Jones         13        2-3       0-0       2-2        1         3         4        1        1        0       0       0        6        1    
     Darren Tuck          4        0-0       0-0       0-0        0         0         0        0        0        0       1       0        0        4    
     Ray Herbert         DNP   
     Derek Smith         DNP   
    Matt Prescott        DNP   
         TEAM                     24-52      2-8      21-28       5         29       34       17       11        8       14      14      71             


       Name           Min       FG        3PT        FT        OREB      DREB      REB      AST      STL      BLK      TO      PF      PTS      +/-   
   Jeremy Allen       29       5-13       0-0        2-3        2         5         7        1        0        0       1       2       12       -7    
   Kevin Bartow       31        3-5       0-0        3-6        0         5         5        1        0        0       2       3        9       -14   
    Mark Givens       27        4-7       4-2        2-2        1         6         7        3        0        0       2       2       12       -6    
   Eddie Carroll      23        3-6       4-2        3-4        0         2         2        3        2        0       0       4       11       -4    
   Jeremy Watson      29        2-4       3-1        0-0        0         2         2        2        0        0       5       2        5       -17   
   Joey Thompson      19        1-6       5-1        3-4        0         1         1        0        0        0       2       1        6       -4    
   Carl Daniels       13        0-4       0-0        0-0        1         1         2        2        0        1       5       1        0       -4    
   Rickie Marek       13        0-1       1-0        3-4        0         2         2        0        1        0       0       1        3       -2    
   Herbert Lloyd      11        1-3       0-0        0-0        0         1         1        0        0        1       0       2        2        0    
   Solomon Leath       1        0-0       0-0        0-0        0         0         0        0        0        0       0       1        0        3    
    Cary Burris       DNP   
    Josh Floyd        DNP   
    Damous King       DNP   
   Daniel Langhi      DNP   
       TEAM                    19-49      6-17      16-23       4         25       29       12        3        2       17      19      60             
```
