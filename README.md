# savage-initiative-tracker
Savage Worlds RPG Initiative Tracker
Author - Parker Nalchajian
Last Updated: 6/26/2018

Version - 1.0
Language - Python 3.6

## Application Functionality ##

- Read in list of characters from file
- Select combatant PCs from list at start of combat
- Remove/Kill combat slot by first going into edit and clicking KILL
- Add multiple default characters (Console app only)
- Add single character
- Print combatant list (Console app only)
- Apply quickness or slow effect
- Application tracks and displays current round of power affecting the character
- Edit characters at any point to apply to the next round of combat
- Click the DEAL button or press <Return> to deal next round
- Automatically orders dealt cards by SW suit order 
- View any character's hand by clicking on their initiative card
- Edit any character by clicking the vertical ellipsis next to their name
- Use any tactician card by clicking on it in the bottom bar

## EDGES ##
### Tactician
- Prompts for Knowledge(battle) roll from a single Tactician
- Deals Tactician cards into persistent Tactician hand location
- User may discard/use tactician cards by clicking on them
**To Do**
+ implement handler for multiple Tacticians
+ implement drag/drop or card assignment when using cards
		List should re-sort after assignment
				
### Level Headed
- Deals two cards from the deck to the character's hand
- Calculates and displays best card from hand
- User may display all cards by clicking on the displayed initiative card

### Improved Level Headed
- Deals three cards from the deck to the character's hand
- Calculates and displays the best card from hand
- User may display all cards by clicking on the displayed initiative card
**To Do**
- Restrict choice to only characters with Level Headed
	
### Quick
- Deals one card at a time to character, re-drawing lower than a Five
	
## POWERS ##
### Quickness (raise)
* No effect on initiative if quickness was not cast with a raise, so 
only trigger this if the casting was 4+ more than the TN
- Deals cards to the character per the pertinent edges. 
- Re-draws cards that are lower in value than an Eight (loop)

### Slow
- Deals cards to the character per the pertinent edges.
- Re-draws cards that are higher in value than a Ten, excluding Jokers (loop)
	
# Unincorporated Long-Term Goals

+ Create host/client functionality to allow members of an adventuring party to
	remotely connect to GM's host and receive cards.
	+ Client-side dice roller
	+ Host-side chat system that allows whispers

+ Add character Sheet functionality that allows for users to track progression
	within the app

+ Incorporate this functionality into a PWA or webapp to divorce it from Python 3.6

+ Allow users to re-skin the interface
	+ New card backs, fronts
	+ Fonts
	+ Size


