FIFA World Cup Draws
==========================================================

### Enviroment versions required:
Python: 2.7  

### Algorithm approach:
Implementing DPLL (Davis–Putnam–Logemann–Loveland) algorithm to generate groups of countries satisfying given constraints. 

### Given constraints:
The draw must satisfy all of the following constraints:  
_C1._ No group can have more than one team from any pot.  
_C2._ No group can have more than one team from any continental confederation, with the exception of UEFA, which can have up to two teams in a group.  
_C3._ There is no limit (minimum or maximum) on the number of teams in each group.  

### Python command for executing DPLL Algorithm

* * *

Exceuting DPLL algorithm using _“Prasad\_Bhagwat\_DPLL.py”_ file

    python Prasad_Bhagwat_DPLL.py <input file path>
    

where,  
_1. 'input file path'_ corresponds to the absolute path of input file  

Example usage of the above command is as follows:

     ~/Desktop Prasad_Bhagwat_DPLL.py /home/prasad/workspace/input.txt
    

Note : _Output file_ named _‘output.txt’_ is generated at the location from where the program is run.

### Input file format:
_C1. GROUP COUNT:_ The number of groups for the FIFA World Cup draw.  
_C2. POT COUNT:_ ​The number of pots for the FIFA World Cup draw.  
_C3. POTS DIVISION:_ ​It contains _POTS COUNT_ lines, where the first line is a comma-separated list of the teams belonging to Pot 1, and the following lines show the teams of Pots 2 to _POTS COUNT_, respectively.  
_C4. TEAMS CONFEDERATION:_ It contains 6 lines where each line begins with the name of one of the ​ continental confederations (AFC, CAF, CONCACAF, CONMEBOL, OFC, or UEFA) followed by a colon “:” and then the names of the teams from this continental confederation separated by commas “,”. If there is no team from a continental confederation, it is denoted by “None”.  

_Example input file:_  
  
6  
6  
England  
Poland  
France  
Russia  
Argentina,Germany  
Italy,Brazil,Mexico  
AFC:None  
OFC:None  
CONCACAF:France,Germany,Italy,England,Russia,Poland  
CONMEBOL:Brazil,Argentina,Mexico  
UEFA:None  

### Output file format:
_YES/NO​:_ A single line containing “Yes” or “No” to indicate whether or not there is a solution for this instance of the 2018 FIFA World Cup draw. If there is a solution, output “Yes” in the first line; otherwise, output only a single line “No”, with nothing else in the output file.  
_SOLUTION:_ If there is a solution after the first line (which is “Yes”) printing _GROUP COUNT_ number of lines, where the first line indicates the names of teams for group 1 separated by commas “,” and so on for groups 2 to _GROUP COUNT_. If there is no team in a specific group, printing “None” for the line corresponding to that group.  

_Example output file:_  
  
Yes  
Germany,Brazil  
France,Mexico  
Russia,Argentina  
England  
Poland  
Italy  
