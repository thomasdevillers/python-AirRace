import sys
import stdarray
import stdio
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = str(1)
# import stddraw
# Standard Draw will only be needed for the second hand-in.

AIRPORTS = 10
INITIAL_BALANCE = 100.0
PLAYERS = 2
MAX_SUITCASE_VAL = 10
SUITCASES_PER_AIRPORT = 4
NUM_OBSTACLE_DISKS = 6
# The number of obstacle disks each player has at the start of the game.
# However, only the red disk should be implemented for the first hand-in.

RED_DISK = 0
GREEN_DISK = 1
YELLOW_DISK = 2
CYAN_DISK = 3
BLACK_DISK = 4
MAGENTA_DISK = 5
# OBSTACLE_DISK_COLOURS = [stddraw.RED, stddraw.GREEN, stddraw.YELLOW, stddraw.CYAN, stddraw.BLACK, stddraw.MAGENTA]
# Colour constants for the obstacle disks for the second hand-in.
OBSTACLE_DISK_STRINGS = ['RED', 'GREEN', 'YELLOW', 'CYAN', 'BLACK', 'MAGENTA']


WALL = '|'
CORN = '+'
LINE = '-'


ERR_TOO_FEW_ARGS = 'Too few command-line arguments were given.'
ERR_TOO_MANY_ARGS = 'Too many command-line arguments were given.'
ERR_UNIMPLEMENTED = 'This feature is not implemented for the current game mode!'
# Use this error message when the player tries to do something that is not yet implemented. This is only relevant during the first hand-in.
# For example, if the value of the command-line argument corresponding to the graphics mode is '1', this error message should be used, because the graphics mode is not yet supported during the first hand-in.
# Similarly, if a player tries to play an obstacle disk that is not supported in the current game mode, this error message should be used.
# NOTE: if a player enters an entirely invalid obstacle disk option, the error message ERR_INVALID_DISK should be used instead.
# Similarly, in game mode 2, players cannot ask their opponent to move from their current airport, so use ERR_UNIMPLEMENTED if they try to do this.

ERR_UNEXPECTED = 'Unexpected input!'
# A generic error message that can be used when the input is unexpected. This will only be used in cases where no other error message is appropriate.
MSG_NO_NEW_GAME_TERMINATION = 'The game has ended.'
ERR_INVALID_TURN_MENU_OPTION = 'Invalid turn menu option!'
ERR_FLOAT_EXPECTED = 'A floating point number was expected!'
# Use this error message we expect a floating point number as input, but the associated value cannot be parsed as a float.
ERR_NOT_YES_OR_NO = 'Expected "Y" or "N" as input!'


ERR_INVALID_AIRPORT = 'Invalid airport!'
ERR_FLYING_TO_SAME_AIRPORT = 'You are already at this airport!'
ERR_FLYING_TO_OPPONENT_AIRPORT = 'You cannot fly to an airport that is occupied by your opponent!'

ERR_FLIPPING_COLLECTED_SUITCASE = 'This suitcase cannot be flipped as it has already been collected.'
ERR_FLIP_RESTRICTED = 'You are not allowed to flip this suitcase. You are trying to flip a suitcase that you have already flipped during your visit.'
ERR_INVALID_SUITCASE_POSITION = 'Invalid suitcase position!'
ERR_INVALID_SUITCASE_NUMBER = 'Invalid suitcase number! The number behind a suitcase must be a value between 1 and 10.'
ERR_BALANCE = 'Insufficient funds!'
ERR_CANT_STAY = 'You cannot stay at this airport! You cannot flip any suitcases here.'
ERR_CANT_ASK = 'You have already asked your opponent if they want to move this turn!'
ERR_EMPTY_STD_INPUT = 'Standard input is empty!'
MSG_USER_TERMINATION = 'Player terminated the game.'

ERR_NO_DISKS = 'You have no obstacle disks that may be played at the moment!'
# Use this error message when the player tries to play an obstacle disk when they have no disks left or cannot currently play any of their remaining disks.
# For example, if the player enters 'U' when asked what they want to do, and they have no obstacle disks left or have already played an obstacle disk during this turn, this error message should be used.
# NOTE: The player can ONLY play the red disk directly after their opponent has refused their request to leave their current airport. If they enter 'U' on the options menu when their opponent has not refused to fly to another airport during this turn, and they have no other disks left, this error message should be used, even if the current player has not yet played their red disk.
# NOTE: This also has other implications. Say the current player has asked their opponent to leave their current airport, and the opponent has refused. Assume the current player has not played their red disk yet. Then, the current player can now play the red disk after they enter 'U' on the options menu. However, no other obstacle disks should be displayed at this point, as the current player can ONLY play their red obstacle disk after their opponent has refused their request to fly to another airport. Even if the current player still has other obstacle disks left, they should not be displayed at this point -- only the red disk should be displayed (assuming you have correctly validated whether or not the red disk can be played according to the specification on when a player can and cannot play the red disk).
# NOTE: Similarly, although mostly related to the requirements for the second hand-in, if the current player selects the 'U' option on the options menu but their opponent was not asked leave their current airport, then ONLY the (available, valid, and implemented) non-red obstacle disks should be displayed -- even if the current player has not yet played their red disk. The red disk may only be displayed directly after the opponent has refused the current player's request to fly to another airport -- in that case, only the red obstacle disk may be displayed, the other obstacle disks cannot be played in the turn where you ask your opponent to fly to another airport. If you don't ask your opponent to fly to another airport, the red disk cannot be played, no matter what.
ERR_INVALID_DISK = 'Invalid obstacle disk option given as input!'
# Use this error message when a player gives an invalid obstacle disk as input. For example, if they are asked to choose which disk to play and they enter 'Z'.
# The following are valid obstacle disk options: ['R', 'G', 'Y', 'C', 'B', 'M']

# NOTE: The following error messages are only relevant for the second hand-in.
ERR_ALREADY_PLAYED_DISK = 'You have already played this obstacle disk!'
# Use this error message when the player tries to play an obstacle disk that they have already played.
ERR_CANT_PLAY_RED_DISK = 'You can only play the red obstacle disk directly after your opponent has refused your request for them to leave their current airport'
# Use this error message when the player tries to play the red disk before their opponent has refused to leave their current airport.
# This may happen when a player enters 'U' when asked what they want to do during their turn, and they enter 'R' to play the red disk even though their opponent had not refused (or been asked) their request to leave during this turn. This will only be relevant for the second hand-in since the 'U' option will not be displayed when the red obstacle disk cannot be played during the first hand-in.
ERR_CANT_PLAY_CYAN_DISK = 'You cannot play the cyan disk until your opponent has moved from their first airport!'
# Use this error message when the player tries to play the cyan disk before their opponent has moved from their first airport.
ERR_CANT_PLAY_MAGENTA_DISK = 'You can only play the magenta disk if your opponent has collected more suitcases that you have.'
# Use this error message when the player tries to play the magenta disk while their opponent has not collected more suitcases than the player has.
ERR_CANT_PLAY_BLACK_DISK = 'You cannot play the black disk when you are not allowed to flip any of the suitcases at your current airport!'
# Use this error message when the player tries to play the black disk when there are no suitcases that they are allowed to flip at their current airport.
# This could happen when the player has already flipped all of the uncollected suitcases during their visit to their current airport.
ERR_MUST_PLAY_HELPFUL_DISK = 'You must play a helpful disk, given your current predicament!'
# Not relevant for the first hand-in.
# Use this error message when the player tries to play a disk that is not helpful to them but the only way for them to avoid losing was to play a helpful obstacle disk. For example, if they have no suitcases left to flip, cannot afford to fly, still have a yellow disk available, and try to play the green disk (which is assumed to be available as well).


MSG_INVALID_GAME_MODE = 'Invalid game mode argument. Using the default value for game_mode instead.'
MSG_INVALID_GRAPHICS_MODE = 'Invalid graphics mode indicator argument. Using the default value for graphics_mode instead.'

ASK_AIRPORT_DESTINATION = 'Player %d, please select the airport you would like to go to. (A-J)\n'
SAY_INITIAL_AIRPORT = 'Player %d has selected Airport %s as their first airport.\n\n'
SAY_FLIGHT_INFO = 'Player %d has flown from Airport %s to Airport %s at a cost of R%.2f.\n\n'

SAY_REQUEST_LEAVE = 'Player %d has asked Player %d if they would like to leave the airport.\n\n'
ASK_WANT_TO_LEAVE = 'Player %d, would you like to leave the airport? (Y/N)\n'
SAY_PLAYER_LEFT = 'Player %d has left their airport upon Player %d\'s request.\n'
SAY_REFUSED_TO_LEAVE = 'Player %d has refused Player %d\'s request to leave their airport.\n\n'

SAY_PLAY_OBSTACLE_DISK = 'Player %d has played their %s obstacle disk.\n\n'
# Print this message when the player plays an obstacle disk. NOTE: The second format specifier represents the name of the obstacle disk that the player played.
# The name of the obstacle disk is one of the following: 'RED', 'GREEN', 'YELLOW', 'CYAN', 'BLACK', or 'MAGENTA'.
# For safety, you can use the array OBSTACLE_DISK_STRINGS alongside the obstacle disk index constants to get the name of the obstacle disk.
# For example, if the player played the red disk, you can use the following code to get the name of the disk:
#   `disk_name = OBSTACLE_DISK_STRINGS[RED_DISK]`
# Then you should call stdio.writef() with the following format string:
#   `stdio.writef(SAY_PLAY_OBSTACLE_DISK, player_index + 1, disk_name)` # Where the value of player_index is 0 for player 1 and 1 for player 2.
# NOTE: Only the red obstacle disk is available during the first hand-in. You only need to use the messages that are relevant to the red obstacle disk during the first hand-in, the other obstacle disks should trigger an error if the player attempts to play any of them.
SAY_RED_DISK = 'Player %d, you are forced to move from your current airport, but Player %d will pay for your flight.\n'
SAY_RED_DISK_DEDUCTION = 'Player %d, you have paid for Player %d\'s flight at a cost of R%.2f. Your new balance is R%.2f\n\n'

ASK_WHICH_OBSTACLE_DISK = 'Player %d, which obstacle disk would you like to use? (R/G/Y/C/B/M)\n'
# This message should be printed when the player is asked to select an obstacle disk to play after they have entered 'U' as their option. See the `show_options()` function for more details.
# NOTE: The red disk is included in this message because it is the ONLY valid obstacle disk option when the current player is asked to select an obstacle disk to play, immediately after their opponent has refused the current player's request to fly to another airport (assuming the other restrictions on when the red obstacle disk can be played are taken into account).
# Players may only play the red disk after their opponent has refused to leave their current airport.
# You should call the `print_obstacle_disks()` function to print the obstacle disks that the player can play after selecting 'U' as their option in `show_options()`.
# If the player uses the 'U' option to print the red obstacle disk after their opponent has refused to leave their current airport, you are not allowed to display any other obstacle disks, even if they are available and valid according to the individual obstacle disk's rules. Only the red disk can be played after the opponent has refused to leave their current airport. This works both ways; if the opponent has not refused to leave their current airport, the current player is not allowed to play the red disk. However, since the other obstacle disks are not implemented during the first hand-in, the restriction is rather simplified for the other obstacle disks. Just make sure you print the correct error message when the player tries to play an obstacle disk that is not available to them at the time.
# TODO: The following messages about the obstacle disks are only relevant to the second hand-in.
SAY_GREEN_DISK = 'The positions of the four suitcases have been shuffled, at each airport.\n\n'
# Print this message when the player plays the green disk.
ASK_YELLOW_DISK_AIRPORT = 'Player %d, please select the airport whose suitcases will be swapped with the suitcases at your current airport. (A-J)\n'
# Ask the player who plays their yellow disk to select an airport whose suitcases will be swapped with the suitcases at their current airport.
SAY_YELLOW_DISK_AIRPORT = 'Player %d has swapped the suitcases of Airport %s with that of Airport %s.\n\n'
# Print this message when the player after the player has selected which airport's suitcases should be swapped with their current airport.
# The first string format specifier represents the player's current airport. The second string format specifier represents the airport whose suitcases were swapped with the player's current airport.
SAY_CYAN_DISK = 'Player %d is forced to pay R%.2f in taxes. Their new balance is R%.2f.\n\n'
# Print this message when the player plays the cyan disk, forcing their opponent to pay taxes equal to the cost of flying from the opponent's previous airport to the opponent's current airport.
SAY_BLACK_DISK = 'The black disk has revealed the following suitcases at Airport %s.\n\n'
# Print this message when the player plays the black disk. Afterwards, you should call the `black_disk_print()` function to print the suitcase numbers that are now revealed at that airport.
SAY_MAGENTA_DISK = 'The magenta disk has added R%.2f to the balance of Player %d. Their new balance is R%.2f.\n\n'
# Print this message when the player plays the magenta disk.

OPT_HEADER = 'Player %d, you can do the following:\n'
OPT_ASK_OPPONENT_TO_MOVE = '\t(A)sk your opponent to leave their airport.'
OPT_STAY_AT_CURRENT_AIRPORT = '\t(S)tay at your current airport.'
OPT_FLY_TO_ANOTHER_AIRPORT = '\t(F)ly to a different airport.'
OPT_USE_OBSTACLE_DISK = '\t(U)se one of your available obstacle disks.\n'

ASK_SUITCASE_POSITION = 'Player %d, please enter the position of the suitcase you would like to flip. (1-4)\n'
SAY_SUITCASE_FLIPPED = 'Player %d has flipped the suitcase at position %d of airport %s to reveal:\n\n'
SAY_COLLECTED = 'Player %d has collected the suitcase at position %d of airport %s.\n\n'
SAY_NOT_COLLECTED = 'Player %d could not collect the suitcase at position %d of airport %s.\n\n'

LOSS_NO_MORE_MOVES = 'Player %d cannot make any more moves!\n'
LOSS_BANKRUPT = 'Player %d has been bankrupted!\n'
WIN_COLLECTED_ALL_SUITCASES = 'Player %d has collected all of their suitcases!\n'
WIN_MESSAGE = 'Player %d has won the game!\n\n'

ASK_NEW_GAME = 'Do you want to start a new game? (Y/N)'
SAY_YES_NEW_GAME = 'A new game is starting!\n'


game_over = False
costMatrix = None

airports = stdarray.create2D(10, 2)
airportAsuitcases = stdarray.create1D(4)
airportBsuitcases = stdarray.create1D(4)
airportCsuitcases = stdarray.create1D(4)
airportDsuitcases = stdarray.create1D(4)
airportEsuitcases = stdarray.create1D(4)
airportFsuitcases = stdarray.create1D(4)
airportGsuitcases = stdarray.create1D(4)
airportHsuitcases = stdarray.create1D(4)
airportIsuitcases = stdarray.create1D(4)
airportJsuitcases = stdarray.create1D(4)

airportAcollected = stdarray.create1D(4, False)
airportBcollected = stdarray.create1D(4, False)
airportCcollected = stdarray.create1D(4, False)
airportDcollected = stdarray.create1D(4, False)
airportEcollected = stdarray.create1D(4, False)
airportFcollected = stdarray.create1D(4, False)
airportGcollected = stdarray.create1D(4, False)
airportHcollected = stdarray.create1D(4, False)
airportIcollected = stdarray.create1D(4, False)
airportJcollected = stdarray.create1D(4, False)

airportAcanFlip = stdarray.create1D(4, True)
airportBcanFlip = stdarray.create1D(4, True)
airportCcanFlip = stdarray.create1D(4, True)
airportDcanFlip = stdarray.create1D(4, True)
airportEcanFlip = stdarray.create1D(4, True)
airportFcanFlip = stdarray.create1D(4, True)
airportGcanFlip = stdarray.create1D(4, True)
airportHcanFlip = stdarray.create1D(4, True)
airportIcanFlip = stdarray.create1D(4, True)
airportJcanFlip = stdarray.create1D(4, True)

player1Airport = ""
player2Airport = ""

player1Balance = INITIAL_BALANCE
player2Balance = INITIAL_BALANCE

usedRedDiskP1 = False
usedRedDiskP2 = False

player1Suitcase = 0
player2Suitcase = 0

player1 = 0
player2 = 1

currentRound = 1

game_mode = 0
graphics_mode = 0


def end_game():
    global game_over
    game_over = True


def int_to_char(index):
    return chr(index + 65)


def char_to_int(ch):
    return ord(str(ch).upper()) - 65


def read_command_line_args():

    game_mode = 0
    graphics_mode = 0

    if len(sys.argv) < 2:
       termination(ERR_TOO_FEW_ARGS)

    if len(sys.argv) > 3:
        termination(ERR_TOO_MANY_ARGS)

    game_mode = int(sys.argv[1])
    graphics_mode = int(sys.argv[2])

    if game_mode != 0 and game_mode != 1:
        # If the game mode is invalid, print this message.
        stdio.write(MSG_INVALID_GAME_MODE)
        game_mode = 0

    if graphics_mode != 0 and graphics_mode != 1:
        # If the graphics mode is invalid, print this message.
        stdio.write(MSG_INVALID_GRAPHICS_MODE)
        graphics_mode = 0

    # TODO: Remove the following if statement for the second hand-in.
    # if the game mode is not 0 or if the graphics mode is not 0, terminate the program.
    if game_mode != 0 or graphics_mode != 0:
        termination(ERR_UNIMPLEMENTED)

    return [game_mode, graphics_mode]


def generate_cost_matrix(airport_coordinates_matrix):
    max_c = float('-inf')
    min_c = float('+inf')
    new_cost_matrix = stdarray.create2D(AIRPORTS, AIRPORTS, 0.0)
    for a1 in range(AIRPORTS):
        new_cost_matrix[a1][a1] = 0.0
        for a2 in range(a1 + 1, AIRPORTS):
            new_cost_matrix[a1][a2] = (
                airport_coordinates_matrix[a1][0] - airport_coordinates_matrix[a2][0])**2
            new_cost_matrix[a1][a2] += (airport_coordinates_matrix[a1]
                                        [1] - airport_coordinates_matrix[a2][1])**2
            new_cost_matrix[a1][a2] = new_cost_matrix[a1][a2]**0.5
            new_cost_matrix[a2][a1] = new_cost_matrix[a1][a2]
            if new_cost_matrix[a2][a1] < min_c:
                min_c = new_cost_matrix[a2][a1]
            if new_cost_matrix[a2][a1] > max_c:
                max_c = new_cost_matrix[a2][a1]
    upper_limit = 20.0
    for a1 in range(AIRPORTS):
        for a2 in range(a1 + 1, AIRPORTS):
            new_cost_matrix[a1][a2] = upper_limit * \
                ((new_cost_matrix[a1][a2] - min_c) / (max_c - min_c))
            new_cost_matrix[a2][a1] = new_cost_matrix[a1][a2]
    return new_cost_matrix


def calculate_magenta_disk_bonus(player_last_suitcase, opponent_last_suitcase):
    """
    Calculates the bonus that the player receives if they play their magenta obstacle disk.

    NOTE: You do not need to use this function during your implementation of the first hand-in. In fact, you should only try to use it if you are done with the implementation for the first hand-in and you want to start with the implementation of the second hand-in early on. The magenta disk should only be implemented for the second hand-in.

    The magenta disk can be played to add money to the player's wallet. The magenta disk only benefits a player if they have collected fewer suitcases than their opponent.
    This function calculates the bonus that the player receives if they play their magenta disk using the following formula:

    Let `x` = the number of suitcases collected by the player who plays the magenta disk.
    Let `y` = the number of suitcases collected by the opponent of the player who plays the magenta disk.
        `bonus = (9 - x) * max(0, y - x)`

    Parameters
    ----------
    player_last_suitcase
        The last suitcase number collected by the player who plays the magenta disk. This is equal to the number of suitcases collected by the player.
    opponent_last_suitcase
        The last suitcase number collected by the opponent of the player who plays the magenta disk. This is equal to the number of suitcases collected by the opponent.

    Returns
    -------
        The bonus that the player receives if they play their magenta disk.
    """
    return (9 - player_last_suitcase) * max(0, opponent_last_suitcase - player_last_suitcase)


def show_options(player, can_ask_opponent_to_leave, canPlayObstacle, usedObstacle, balance, costMatrix, game_mode, p1Airport, p2Airport):
    if game_mode == 2:
        # Furthermore, when the game_mode variable is set to 2, indicating AI game-play, then the (AI) players cannot use obstacle disks.
        can_play_obstacle = False
        can_ask_opponent_to_leave = False

    if player == 0: #checks what the player value passed in via the parameter to determine which airports to work with
        airport = p1Airport
        oppAir = p2Airport
    else:
        airport = p2Airport
        oppAir = p1Airport

    if balance > calculateMinFlightCost(airport, costMatrix, oppAir): #checks if the player has enough money to fly to the any other airport
        can_fly = True
    else:
        can_fly = False

    if (assignAirportCollectedSuitcases(airport)[0] == True or assignAirportCanFlip(airport)[0] == False) and (assignAirportCollectedSuitcases(airport)[1] == True or assignAirportCanFlip(airport)[1] == False) and (assignAirportCollectedSuitcases(airport)[2] == True or assignAirportCanFlip(airport)[2] == False) and (assignAirportCollectedSuitcases(airport)[3] == True or assignAirportCanFlip(airport)[3] == False): 
        #checks the status of the canFlip and collectedSuitcases arrays for the current airport to determine whether the player can stay at their current airport
        can_stay = False
    else:
        can_stay = True

    # The four Boolean variables above indicate whether the player can do the corresponding action.
    # For example, if the player can ask the opponent to leave their airport, then the can_ask_opponent_to_leave variable will be set to True.
    #               This may be false if the player has already asked the opponent to leave their airport during this round.
    # The can_fly variable indicates whether the player can fly to another airport.
    # The can_stay variable indicates whether the player can stay at their current airport.
    # The can_play_obstacle variable indicates whether the player can play an obstacle disk.
    # NOTE: the current player can only play the red obstacle disk immediately after their opponent has refused the current player's request to fly to another airport -- assuming the current player has not yet played their red disk.
    # For the first hand-in, only the red obstacle disk is implemented. A player can only play the red obstacle disk when they have already asked the opponent to leave their airport, and the opponent has refused to leave. This implies that the red obstacle disk is only displayed sometimes!
    # When the show_options function is called after the opponent has refused to fly to a different airport, the current player will be able to select the 'U' option, but it will only display the red obstacle disk (assuming the current player has not played the red disk yet) -- no other disks should be displayed in this case!
    # If the current player has already used their red obstacle disk, the 'U' option should not be displayed after calling show_options after the opponent has refused the current player's request.
    # If the current player did not ask their opponent to leave their airport, the 'U' option should only display the other obstacle disks (depending on the non-red disks' availabilities), even if the player has not used the red disk yet.
    # Since the other disks will only be implemented for the second hand-in, only the red disk should be displayed here (noting the aforementioned rules about when the red disk can be used).

    if can_stay == False and can_fly == False and player == 0: #if the player cant stay and cant fly, they lose (if player == 0 then player 1 looses)
        stdio.write(LOSS_NO_MORE_MOVES % (1))
        stdio.write(WIN_MESSAGE % (2))
        stdio.writeln(ASK_NEW_GAME)
        newGame = stdio.readString()
        if newGame == "Y": #checks if the player wants to play a new game
            stdio.writeln(SAY_YES_NEW_GAME)
            game()
        else:
            termination(MSG_NO_NEW_GAME_TERMINATION)

    if can_stay == False and can_fly == False and player == 1: # if the player cant stay and cant fly, they lose (if player == 1 then player 2 looses)
        stdio.write(LOSS_NO_MORE_MOVES % (2))
        stdio.write(WIN_MESSAGE % (1))
        stdio.writeln(ASK_NEW_GAME)
        newGame = stdio.readString()
        if newGame == "Y":
            stdio.writeln(SAY_YES_NEW_GAME)
        else:
            termination(MSG_NO_NEW_GAME_TERMINATION)

    stdio.writef(OPT_HEADER, player + 1)
    if can_ask_opponent_to_leave: # if the player can ask the opponent to leave, then the option to ask the opponent to leave is displayed
        stdio.writeln(OPT_ASK_OPPONENT_TO_MOVE)
    if can_stay: # if the player can stay, then the option to stay is displayed
        stdio.writeln(OPT_STAY_AT_CURRENT_AIRPORT)
    if can_fly: # if the player can fly, then the option to fly is displayed
        stdio.writeln(OPT_FLY_TO_ANOTHER_AIRPORT)
    if usedObstacle == False and canPlayObstacle: # if the player can play an obstacle disk and hasnt used his obstacle disk yet, then the option to play an obstacle disk is displayed
        stdio.writeln(OPT_USE_OBSTACLE_DISK)
        can_play_red = True
        # TODO: You will need to add similar functionality for the other non-red disks during your implementation of the second hand-in.
        can_play_disk_array = [can_play_red, False, False, False, False, False]
        print_obstacle_disks(can_play_disk_array)
        # The majority of the `print_obstacle_disks` function is mainly applicable to the second hand-in, since the red disk is the only obstacle disk implemented for the first hand-in. Ensure that you understand when you need to display the red obstacle using `print_obstacle_disks` disk, however!
    stdio.writeln()  # DONT REMOVE

    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT)
    response = stdio.readString() 
    if response == "Q":
        termination(MSG_USER_TERMINATION)
    return response #users choice is returned


def calculateMinFlightCost(currentAirport, matrix, oppAirport):
    smallest = 100
    for x in range(0, 10):
        num = matrix[x][ord(currentAirport) - ord('A')]
        if num < smallest and num != matrix[x][ord(oppAirport) - ord('A')]:
            smallest = num
    return round(smallest, 2)
# This function calculates the minimum flight cost from the current airport to any other airport, excluding the opponent's airport.

def modifySuitcaseFlipped(playerAirport, suitcasePos):
    airports = [airportAcollected, airportBcollected, airportCcollected,
                airportDcollected, airportEcollected, airportFcollected,
                airportGcollected, airportHcollected, airportIcollected,
                airportJcollected]

    playerAirportIndex = ord(playerAirport) - ord('A')
    airports[playerAirportIndex][suitcasePos - 1] = True
# This function modifies the suitcase flipped variable to True, indicating that the suitcase has been flipped.

def assignAirport(airportLetter):
    airportList = [airportAsuitcases, airportBsuitcases, airportCsuitcases,
                   airportDsuitcases, airportEsuitcases, airportFsuitcases,
                   airportGsuitcases, airportHsuitcases, airportIsuitcases,
                   airportJsuitcases]

    return airportList[ord(airportLetter) - ord('A')]
# This function returns an array of the specific suitcases at an airport depending on which airport the player is at

def assignAirportCollectedSuitcases(airportLetter):
    airportList = [airportAcollected, airportBcollected, airportCcollected,
                   airportDcollected, airportEcollected, airportFcollected,
                   airportGcollected, airportHcollected, airportIcollected,
                   airportJcollected]

    index = ord(airportLetter) - ord("A")
    return airportList[index]
# This function returns an array of booleans indicating which suitcases have been flipped at a specific airport

def assignAirportCanFlip(airportLetter):
    canFlipList = [airportAcanFlip, airportBcanFlip, airportCcanFlip,
                   airportDcanFlip, airportEcanFlip, airportFcanFlip,
                   airportGcanFlip, airportHcanFlip, airportIcanFlip,
                   airportJcanFlip]

    index = ord(airportLetter) - ord("A")
    return canFlipList[index]
# This function returns an array of booleans indicating which suitcases can be flipped at a specific airport

def check_stdio_empty():
    """
    Check whether standard input is empty. If it is, terminate the game and display the associated error message.
    The code within this function should give you an idea of how you should terminate the program when an error occurs, using the appropriate error message.
    You are not required to use this function, but you MUST use the variable `ERR_EMPTY_STD_INPUT` to terminate the program using the error message associated with an empty standard input.
    """
    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT)

def is_float(s):
    for i in range (len(s)):
        if not (s[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "E", "-", "."]):
            termination(ERR_FLOAT_EXPECTED)


def resetVariables():
    player1Airport = ""
    player2Airport = ""

    player1Balance = INITIAL_BALANCE
    player2Balance = INITIAL_BALANCE

    usedRedDiskP1 = False
    usedRedDiskP2 = False

    player1Suitcase = 0
    player2Suitcase = 0

    currentRound = 1

    for i in range(4):
        airportAcollected[i] = False
        airportBcollected[i] = False
        airportCcollected[i] = False
        airportDcollected[i] = False
        airportEcollected[i] = False
        airportFcollected[i] = False
        airportGcollected[i] = False
        airportHcollected[i] = False
        airportIcollected[i] = False
        airportJcollected[i] = False
        airportAcanFlip[i] = True
        airportBcanFlip[i] = True
        airportCcanFlip[i] = True
        airportDcanFlip[i] = True
        airportEcanFlip[i] = True
        airportFcanFlip[i] = True
        airportGcanFlip[i] = True
        airportHcanFlip[i] = True
        airportIcanFlip[i] = True
        airportJcanFlip[i] = True
# This function resets all the variables to their default values

def runner():
    game_mode, graphics_mode = read_command_line_args()

    print_command_line_args(game_mode, graphics_mode)
    for line in range(0, 10): #loops through the 10 groups of information (2 coords and 4 suitcase numbers) in the input file
        tempArr = ["", "", "", "", "", ""] #temporary list to store each group of information
        for part in range(0, 6): #loops through the 6 parts in a single group
            check_stdio_empty()
            tempArr[part] = stdio.readString() #populates the list with items from each group
            if tempArr[part] == "Q": #checks if each part is Q and in that case program quits
                termination(MSG_USER_TERMINATION)
            if is_float(tempArr[part]) == False and (part == 0 or part == 1) and tempArr[part] != "Q":
                termination(ERR_FLOAT_EXPECTED)
        airports[line][0] = float(tempArr[0]) #populates the 2D array with the airport coordinates
        airports[line][1] = float(tempArr[1])

        airportSuit = [airportAsuitcases, airportBsuitcases, airportCsuitcases, airportDsuitcases,
                       airportEsuitcases, airportFsuitcases, airportGsuitcases, airportHsuitcases,
                       airportIsuitcases, airportJsuitcases]
        suitcases = airportSuit[line]
        suitcases[0] = tempArr[2]
        suitcases[1] = tempArr[3]
        suitcases[2] = tempArr[4]
        suitcases[3] = tempArr[5]
        #the above code populates every array of airport suitcases with the numbers from the input file

    game() #calls the game function for main gameplay


def game():
    # NB
    # for simplicity, repeated code is only commented once (at the time its first used)
    # predefined functions are also excluded eg. print_airport_grid etc.
    # therefore as you scroll down comments become more scarce

    resetVariables()
    usedRedDiskP1 = False
    usedRedDiskP2 = False

    costMatrix = generate_cost_matrix(airports) #generates cost matrix and assigns it to a variable
    currentRound = 1
    player1Suitcase = 0
    player2Suitcase = 0
    player1Balance = 100
    player2Balance = 100 #default values for variables
    print_cost_matrix(costMatrix, player1, player1Balance, currentRound)
    stdio.write(ASK_AIRPORT_DESTINATION % (1))
    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT)
    player1Airport = stdio.readString() #
    if player1Airport == "Q": #checks if input is "Q", if so program quits
        termination(MSG_USER_TERMINATION)
    if player1Airport not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"): #checks that the airport choice is valid
        termination(ERR_INVALID_AIRPORT)
    stdio.write(SAY_INITIAL_AIRPORT % (1, player1Airport))
    print_airport_grid(char_to_int(player1Airport), -1)
    print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
        player1Airport), assignAirportCanFlip(player1Airport))
    print_suitcase_grid(player1Suitcase, player2Suitcase)
    stdio.write(ASK_SUITCASE_POSITION % (1))
    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT) #checks if standard input is empty
    suitcaseFlipped = stdio.readString()
    if suitcaseFlipped == "Q":
        termination(MSG_USER_TERMINATION)
    if suitcaseFlipped not in ("1", "2", "3", "4"): #checks that user entered a valid suitcase number
        termination(ERR_INVALID_SUITCASE_POSITION)
    suitcaseFlipped = int(suitcaseFlipped) #converts suitcase number to an int
    assignAirportCanFlip(player1Airport)[suitcaseFlipped-1] = False # applies the flip restriction to a specific suitcase when its been flipped
    stdio.write(SAY_SUITCASE_FLIPPED % (1, suitcaseFlipped, player1Airport))
    print_single_suitcase_number(
        assignAirport(player1Airport)[suitcaseFlipped-1])
    if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase: #checks whether or not the suitcase flipped can be collected by comparing the suitcase number to the number of suitcases the player has previously collected
        stdio.write(SAY_COLLECTED % (1, suitcaseFlipped, player1Airport))
        modifySuitcaseFlipped(player1Airport, suitcaseFlipped) # marks the specific suitcase that has been collected as collected by modifying the boolean value in the array that stores whether or not specific suitcases have been collected from a specific airport
        assignAirportCanFlip(player1Airport)[0] = True #resets the flip restriction as player has successfuly collected a suitcase
        assignAirportCanFlip(player1Airport)[1] = True
        assignAirportCanFlip(player1Airport)[2] = True
        assignAirportCanFlip(player1Airport)[3] = True
        player1Suitcase += 1 #increases players suitcase counts since they successfully collected a suitcase
    else:
        stdio.write(SAY_NOT_COLLECTED % (1, suitcaseFlipped, player1Airport))
    print_suitcase_grid(player1Suitcase, player2Suitcase)

    print_cost_matrix(costMatrix, player2, player2Balance, currentRound)
    stdio.write(ASK_AIRPORT_DESTINATION % (2))
    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT)
    player2Airport = stdio.readString()
    if player2Airport == "Q":
        termination(MSG_USER_TERMINATION)
    if player2Airport not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
        termination(ERR_INVALID_AIRPORT)
    if player2Airport == player1Airport:
        termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
    stdio.write(SAY_INITIAL_AIRPORT % (2, player2Airport))
    print_airport_grid(char_to_int(player1Airport),
                       char_to_int(player2Airport))
    print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
        player2Airport), assignAirportCanFlip(player2Airport))
    print_suitcase_grid(player1Suitcase, player2Suitcase)
    stdio.write(ASK_SUITCASE_POSITION % (2))
    if stdio.isEmpty():
        termination(ERR_EMPTY_STD_INPUT)
    suitcaseFlipped = stdio.readString()
    if suitcaseFlipped == "Q":
        termination(MSG_USER_TERMINATION)
    if suitcaseFlipped not in ("1", "2", "3", "4"):
        termination(ERR_INVALID_SUITCASE_POSITION)
    suitcaseFlipped = int(suitcaseFlipped)
    assignAirportCanFlip(player2Airport)[suitcaseFlipped-1] = False
    stdio.write(SAY_SUITCASE_FLIPPED % (2, suitcaseFlipped, player2Airport))
    print_single_suitcase_number(
        assignAirport(player2Airport)[suitcaseFlipped-1])
    if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
        stdio.write(SAY_COLLECTED % (2, suitcaseFlipped, player2Airport))
        assignAirportCanFlip(player2Airport)[0] = True
        assignAirportCanFlip(player2Airport)[1] = True
        assignAirportCanFlip(player2Airport)[2] = True
        assignAirportCanFlip(player2Airport)[3] = True
        modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
        player2Suitcase += 1
    else:
        stdio.write(SAY_NOT_COLLECTED % (2, suitcaseFlipped, player2Airport))
    currentRound += 1 #increases round count as first round has ended
    print_suitcase_grid(player1Suitcase, player2Suitcase)
    currentPlayer = 0 #sets current player to 0 which indicates its player 1's turn next

    while not game_over:

        print_cost_matrix(costMatrix, player1, player1Balance, currentRound)
        print_airport_grid(char_to_int(player1Airport),
                           char_to_int(player2Airport))
        playerResponse = show_options(currentPlayer, True, False, usedRedDiskP1,
                                 player1Balance, costMatrix, game_mode, player1Airport, player2Airport) #displays available options to player and returns their response which is set equal to a variable
        if playerResponse not in ("A", "F", "S", "U"): #checks if a users response is valid or not, if not program terminates
            termination(ERR_INVALID_TURN_MENU_OPTION)
        if playerResponse == "U": #checks if user selected "U", if so program terminates
            termination(ERR_NO_DISKS)
        if playerResponse == "A": #checks if users response is A, if so following code applies...
            stdio.write(SAY_REQUEST_LEAVE % (1, 2))
            stdio.write(ASK_WANT_TO_LEAVE % (2))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            playerAnswer = stdio.readString()
            if playerAnswer == "Q":
                termination(MSG_USER_TERMINATION)
            if playerAnswer != "Y" and playerAnswer != "N": #checks whether users response is either Y or N, if not program terminates
                termination(ERR_NOT_YES_OR_NO)
            if playerAnswer == "Y": # if users response is Y, following code applies...
                stdio.write(SAY_PLAYER_LEFT % (2, 1))
                stdio.write(ASK_AIRPORT_DESTINATION % (2))
                if stdio.isEmpty():
                    termination(ERR_EMPTY_STD_INPUT)
                ap = stdio.readString()
                if ap == "Q":
                    termination(MSG_USER_TERMINATION)
                if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                    termination(ERR_INVALID_AIRPORT)
                if ap == player2Airport: # checks if user is trying to fly to the same airport they are currently at, if so program terminates
                    termination(ERR_FLYING_TO_SAME_AIRPORT)
                if ap == player1Airport: # checks if user is trying to fly to the same airport as the other player, if so program terminates
                    termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                flightCost = costMatrix[int(char_to_int(
                    player2Airport))][int(char_to_int(ap))] #calculates flight cost
                stdio.write(SAY_FLIGHT_INFO % (2, player2Airport, ap, 0))
                assignAirportCanFlip(player2Airport)[0] = True #resets players flip restriction as they accepted the request to fly to a new airport
                assignAirportCanFlip(player2Airport)[1] = True
                assignAirportCanFlip(player2Airport)[2] = True
                assignAirportCanFlip(player2Airport)[3] = True
                player2Airport = ap # changes players airport to the one they selected
                print_airport_grid(char_to_int(player1Airport),
                                   char_to_int(player2Airport))
                print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                    player2Airport), assignAirportCanFlip(player2Airport))
                print_suitcase_grid(player1Suitcase, player2Suitcase)
                stdio.write(ASK_SUITCASE_POSITION % (2))
                if stdio.isEmpty():
                    termination(ERR_EMPTY_STD_INPUT)
                suitcaseFlipped = stdio.readString()
                if suitcaseFlipped == "Q":
                    termination(MSG_USER_TERMINATION)
                if suitcaseFlipped not in ("1", "2", "3", "4"):
                    termination(ERR_INVALID_SUITCASE_POSITION)
                suitcaseFlipped = int(suitcaseFlipped)
                if assignAirportCollectedSuitcases(player2Airport)[suitcaseFlipped - 1]:
                    termination(ERR_FLIPPING_COLLECTED_SUITCASE)
                stdio.write(SAY_SUITCASE_FLIPPED %
                            (2, suitcaseFlipped, player2Airport))
                print_single_suitcase_number(
                    assignAirport(player2Airport)[suitcaseFlipped-1])
                assignAirportCanFlip(player2Airport)[suitcaseFlipped-1] = False
                if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                    stdio.write(SAY_COLLECTED % (2, suitcaseFlipped, player2Airport))
                    modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                    assignAirportCanFlip(player2Airport)[0] = True
                    assignAirportCanFlip(player2Airport)[1] = True
                    assignAirportCanFlip(player2Airport)[2] = True
                    assignAirportCanFlip(player2Airport)[3] = True
                    player2Suitcase += 1
                    if player2Suitcase == 10: #checks if player has collected all 10 suitcases, if so following code applies...
                        print_suitcase_grid(player1Suitcase, player2Suitcase)
                        stdio.write(WIN_COLLECTED_ALL_SUITCASES % (2))
                        stdio.write(WIN_MESSAGE % (2))
                        stdio.writeln(ASK_NEW_GAME)
                        if stdio.isEmpty():
                            termination(ERR_EMPTY_STD_INPUT)
                        newGame = stdio.readString()
                        if newGame == "Q": # checks if user wants to quit, if so program terminates
                            termination(MSG_USER_TERMINATION)
                        if newGame == "Y": # checks if user wants to play a new game, if so following code applies...
                            stdio.writeln(SAY_YES_NEW_GAME)
                            game() # calls game function
                        else: # if user does not want to play a new game, program terminates
                            termination(MSG_NO_NEW_GAME_TERMINATION)
                else:
                    stdio.write(SAY_NOT_COLLECTED % (2, suitcaseFlipped, player2Airport))
                print_suitcase_grid(player1Suitcase, player2Suitcase)
                playerResponse = show_options(currentPlayer, False, False, usedRedDiskP1,
                                         player1Balance, costMatrix, game_mode, player1Airport, player2Airport) # recalls show_options method to allow user to select an additional option
                if playerResponse == "A": # checks if user chose "A", if so program terminates
                    termination(ERR_CANT_ASK)
            elif playerAnswer == "N": # if users response is N, following code applies..
                stdio.write(SAY_REFUSED_TO_LEAVE % (2, 1))
                response = show_options(0, False, True, usedRedDiskP1, player1Balance,
                                        costMatrix, game_mode, player1Airport, player2Airport)
                if response == "S": # checks if user chose "S", if so following code applies...
                    if (assignAirportCanFlip(player1Airport)[0] == False or assignAirportCollectedSuitcases(player1Airport)[0] == True) and (assignAirportCanFlip(player1Airport)[1] == False or assignAirportCollectedSuitcases(player1Airport)[1] == True) and (assignAirportCanFlip(player1Airport)[2] == False or assignAirportCollectedSuitcases(player1Airport)[2] == True) and (assignAirportCanFlip(player1Airport)[3] == False or assignAirportCollectedSuitcases(player1Airport)[3] == True):
                        termination(ERR_CANT_STAY)
                    print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                        player1Airport), assignAirportCanFlip(player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (1, suitcaseFlipped, player1Airport))
                    assignAirportCanFlip(player1Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player1Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                        modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                        assignAirportCanFlip(player1Airport)[0] = True
                        assignAirportCanFlip(player1Airport)[1] = True
                        assignAirportCanFlip(player1Airport)[2] = True
                        assignAirportCanFlip(player1Airport)[3] = True
                        player1Suitcase += 1
                        if player1Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                            stdio.write(WIN_MESSAGE % (1))
                            stdio.write(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                if response == "F":
                    assignAirportCanFlip(player1Airport)[0] = True # resets flip restriction as player has flown to a new airport
                    assignAirportCanFlip(player1Airport)[1] = True
                    assignAirportCanFlip(player1Airport)[2] = True
                    assignAirportCanFlip(player1Airport)[3] = True
                    stdio.write(ASK_AIRPORT_DESTINATION % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    ap = stdio.readString()
                    if ap == "Q":
                        termination(MSG_USER_TERMINATION)
                    if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                        termination(ERR_INVALID_AIRPORT)
                    if ap == player1Airport:
                        termination(ERR_FLYING_TO_SAME_AIRPORT)
                    if ap == player2Airport:
                        termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                    flightCost = costMatrix[int(char_to_int(
                        player1Airport))][int(char_to_int(ap))]
                    if flightCost > player1Balance: # checks if player has enough money to fly to new airport, if not program terminates
                        termination(ERR_BALANCE)
                    stdio.writen(SAY_FLIGHT_INFO %
                                 (1, player1Airport, ap, flightCost))
                    player1Airport = ap
                    player1Balance = player1Balance - flightCost # subtracts flight cost from player balance
                    print_airport_grid(char_to_int(
                        player1Airport), char_to_int(player2Airport))
                    print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                        player1Airport), assignAirportCanFlip(player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (1, suitcaseFlipped, player1Airport))
                    assignAirportCanFlip(player1Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player1Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                        modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                        assignAirportCanFlip(player1Airport)[0] = True
                        assignAirportCanFlip(player1Airport)[1] = True
                        assignAirportCanFlip(player1Airport)[2] = True
                        assignAirportCanFlip(player1Airport)[3] = True
                        player1Suitcase += 1
                        if player1Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                            stdio.write(WIN_MESSAGE % (1))
                            stdio.writeln(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                if response == "U":
                    if usedRedDiskP1 == True: # checks if player has already used red disk, if so program terminates
                        termination(ERR_NO_DISKS)
                    stdio.write(ASK_WHICH_OBSTACLE_DISK % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    choice = stdio.readString()
                    if choice == "Q":
                        termination(MSG_USER_TERMINATION)
                    if choice not in ('R', 'G', 'Y', 'C', 'B', 'M'): # checks if player has entered a valid disk, if not program terminates
                        termination(ERR_INVALID_DISK)
                    if choice != "R": # checks if player has entered anything but a red disk, if so program terminates
                        termination(ERR_UNIMPLEMENTED)
                    usedRedDiskP1 = True # sets used red disk to true
                    # change this for 2nd hand in
                    stdio.write(SAY_PLAY_OBSTACLE_DISK %
                                (1, OBSTACLE_DISK_STRINGS[RED_DISK]))
                    stdio.write("") #gap between obstacle disk and and text
                    stdio.write(SAY_RED_DISK % (2, 1))
                    stdio.write(ASK_AIRPORT_DESTINATION % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    ap = stdio.readString()
                    if ap == "Q":
                        termination(MSG_USER_TERMINATION)
                    if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                        termination(ERR_INVALID_AIRPORT)
                    if ap == player1Airport:
                        termination(ERR_FLYING_TO_SAME_AIRPORT)
                    if ap == player2Airport:
                        termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                    flightCost = costMatrix[int(char_to_int(
                        player2Airport))][int(char_to_int(ap))]
                    if flightCost > player1Balance: #checks if player 1 has enough money to cover player 2's flight, if not program terminates
                        termination(ERR_BALANCE)
                    stdio.write(SAY_FLIGHT_INFO % (2, player2Airport, ap, 0))
                    assignAirportCanFlip(player2Airport)[0] = True #resets player 2's flip restriction as player 2 is forced to fly to a new airport
                    assignAirportCanFlip(player2Airport)[1] = True
                    assignAirportCanFlip(player2Airport)[2] = True
                    assignAirportCanFlip(player2Airport)[3] = True
                    player2Airport = ap
                    player1Balance = player1Balance - flightCost

                    print_airport_grid(char_to_int(
                        player1Airport), char_to_int(player2Airport))
                    print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                        player2Airport), assignAirportCanFlip(player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (2, suitcaseFlipped, player2Airport))
                    assignAirportCanFlip(player2Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player2Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                        modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                        assignAirportCanFlip(player2Airport)[0] = True
                        assignAirportCanFlip(player2Airport)[1] = True
                        assignAirportCanFlip(player2Airport)[2] = True
                        assignAirportCanFlip(player2Airport)[3] = True
                        player2Suitcase += 1
                        if player2Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (2))
                            stdio.write(WIN_MESSAGE % (2))
                            stdio.writeln(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(SAY_RED_DISK_DEDUCTION %
                                (1, 2, flightCost, player1Balance))
                    playerResponse = show_options(currentPlayer, False, False, usedRedDiskP1,
                                             player1Balance, costMatrix, game_mode, player1Airport, player2Airport)

        if playerResponse == "S":
            if (assignAirportCanFlip(player1Airport)[0] == False or assignAirportCollectedSuitcases(player1Airport)[0] == True) and (assignAirportCanFlip(player1Airport)[1] == False or assignAirportCollectedSuitcases(player1Airport)[1] == True) and (assignAirportCanFlip(player1Airport)[2] == False or assignAirportCollectedSuitcases(player1Airport)[2] == True) and (assignAirportCanFlip(player1Airport)[3] == False or assignAirportCollectedSuitcases(player1Airport)[3] == True):
                termination(ERR_CANT_STAY) #checks if player 1 can stay at the airport, if not program terminates
            print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                player1Airport), assignAirportCanFlip(player1Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)
            stdio.write(ASK_SUITCASE_POSITION % (1))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            suitcaseFlipped = stdio.readString()
            if suitcaseFlipped == "Q":
                termination(MSG_USER_TERMINATION)
            if suitcaseFlipped not in ("1", "2", "3", "4"):
                termination(ERR_INVALID_SUITCASE_POSITION)
            suitcaseFlipped = int(suitcaseFlipped)
            if assignAirportCanFlip(player1Airport)[suitcaseFlipped-1] == False:
                termination(ERR_FLIP_RESTRICTED)
            stdio.write(SAY_SUITCASE_FLIPPED %
                        (1, suitcaseFlipped, player1Airport))
            assignAirportCanFlip(player1Airport)[suitcaseFlipped-1] = False
            print_single_suitcase_number(
                assignAirport(player1Airport)[suitcaseFlipped-1])
            if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                stdio.write(SAY_COLLECTED %
                            (1, suitcaseFlipped, player1Airport))
                modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                assignAirportCanFlip(player1Airport)[0] = True
                assignAirportCanFlip(player1Airport)[1] = True
                assignAirportCanFlip(player1Airport)[2] = True
                assignAirportCanFlip(player1Airport)[3] = True
                player1Suitcase += 1
                if player1Suitcase == 10:
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                    stdio.write(WIN_MESSAGE % (1))
                    stdio.writeln(ASK_NEW_GAME)
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    newGame = stdio.readString()
                    if newGame == "Q":
                        termination(MSG_USER_TERMINATION)
                    if newGame == "Y":
                        stdio.writeln(SAY_YES_NEW_GAME)
                        game()
                    else:
                        termination(MSG_NO_NEW_GAME_TERMINATION)
            else:
                stdio.write(SAY_NOT_COLLECTED %
                            (1, suitcaseFlipped, player1Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)

        if playerResponse == "F":
            assignAirportCanFlip(player1Airport)[0] = True #resets players flip restriction as they chose to fly to a new airport
            assignAirportCanFlip(player1Airport)[1] = True
            assignAirportCanFlip(player1Airport)[2] = True
            assignAirportCanFlip(player1Airport)[3] = True
            stdio.write(ASK_AIRPORT_DESTINATION % (1))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            ap = stdio.readString()
            if ap == "Q":
                termination(MSG_USER_TERMINATION)
            if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                termination(ERR_INVALID_AIRPORT)
            if ap == player1Airport:
                termination(ERR_FLYING_TO_SAME_AIRPORT)
            if ap == player2Airport:
                termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
            flightCost = costMatrix[int(char_to_int(
                player1Airport))][int(char_to_int(ap))]
            if flightCost > player1Balance:
                termination(ERR_BALANCE)
            stdio.write(SAY_FLIGHT_INFO % (1, player1Airport, ap, flightCost))
            player1Airport = ap
            player1Balance = player1Balance - flightCost
            print_airport_grid(char_to_int(player1Airport),
                               char_to_int(player2Airport))
            print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                player1Airport), assignAirportCanFlip(player1Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)
            stdio.write(ASK_SUITCASE_POSITION % (1))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            suitcaseFlipped = stdio.readString()
            if suitcaseFlipped == "Q":
                termination(MSG_USER_TERMINATION)
            if suitcaseFlipped not in ("1", "2", "3", "4"):
                termination(ERR_INVALID_SUITCASE_POSITION)
            suitcaseFlipped = int(suitcaseFlipped)
            stdio.write(SAY_SUITCASE_FLIPPED %
                        (1, suitcaseFlipped, player1Airport))
            assignAirportCanFlip(player1Airport)[suitcaseFlipped-1] = False
            print_single_suitcase_number(
                assignAirport(player1Airport)[suitcaseFlipped-1])
            if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                stdio.write(SAY_COLLECTED %
                            (1, suitcaseFlipped, player1Airport))
                modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                assignAirportCanFlip(player1Airport)[0] = True
                assignAirportCanFlip(player1Airport)[1] = True
                assignAirportCanFlip(player1Airport)[2] = True
                assignAirportCanFlip(player1Airport)[3] = True
                player1Suitcase += 1
                if player1Suitcase == 10:
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                    stdio.write(WIN_MESSAGE % (1))
                    stdio.writeln(ASK_NEW_GAME)
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    newGame = stdio.readString()
                    if newGame == "Q":
                        termination(MSG_USER_TERMINATION)
                    if newGame == "Y":
                        stdio.writeln(SAY_YES_NEW_GAME)
                        game()
                    else:
                        termination(MSG_NO_NEW_GAME_TERMINATION)
            else:
                stdio.write(SAY_NOT_COLLECTED %
                            (1, suitcaseFlipped, player1Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)

        currentPlayer = currentPlayer + 1 # updates the current player value (increased from 0 to 1 now and decreased from 1 to 0 at the end of player 2's turn)
        print_cost_matrix(costMatrix, player2, player2Balance, currentRound)
        print_airport_grid(char_to_int(player1Airport),
                           char_to_int(player2Airport))
        
        # code for player 2 is similar as player 1's code except for the values of the variables therefore I will not repeat comments
        playerResponse = show_options(currentPlayer, True, False, usedRedDiskP2,
                                 player2Balance, costMatrix, game_mode, player1Airport, player2Airport)

        if playerResponse not in ("A", "F", "S", "U"):
            termination(ERR_INVALID_TURN_MENU_OPTION)
        if playerResponse == "U":
            termination(ERR_NO_DISKS)
        if playerResponse == "A":
            stdio.write(SAY_REQUEST_LEAVE % (2, 1))
            stdio.write(ASK_WANT_TO_LEAVE % (1))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            playerAnswer = stdio.readString()
            if playerAnswer == "Q":
                termination(MSG_USER_TERMINATION)
            if playerAnswer != "Y" and playerAnswer != "N":
                termination(ERR_NOT_YES_OR_NO)
            if playerAnswer == "Y":
                stdio.write(SAY_PLAYER_LEFT % (1, 2))
                stdio.write(ASK_AIRPORT_DESTINATION % (1))
                if stdio.isEmpty():
                    termination(ERR_EMPTY_STD_INPUT)
                ap = stdio.readString()
                if ap == "Q":
                    termination(MSG_USER_TERMINATION)
                if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                    termination(ERR_INVALID_AIRPORT)
                if ap == player1Airport:
                    termination(ERR_FLYING_TO_SAME_AIRPORT)
                if ap == player2Airport:
                    termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                flightCost = costMatrix[int(char_to_int(
                    player1Airport))][int(char_to_int(ap))]
                stdio.write(SAY_FLIGHT_INFO % (1, player1Airport, ap, 0))
                assignAirportCanFlip(player1Airport)[0] = True
                assignAirportCanFlip(player1Airport)[1] = True
                assignAirportCanFlip(player1Airport)[2] = True
                assignAirportCanFlip(player1Airport)[3] = True
                player1Airport = ap
                print_airport_grid(char_to_int(player1Airport),
                                   char_to_int(player2Airport))
                print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                    player1Airport), assignAirportCanFlip(player1Airport))
                print_suitcase_grid(player1Suitcase, player2Suitcase)
                stdio.write(ASK_SUITCASE_POSITION % (1))
                if stdio.isEmpty():
                    termination(ERR_EMPTY_STD_INPUT)
                suitcaseFlipped = stdio.readString()
                if suitcaseFlipped == "Q":
                    termination(MSG_USER_TERMINATION)
                if suitcaseFlipped not in ("1", "2", "3", "4"):
                    termination(ERR_INVALID_SUITCASE_POSITION)
                suitcaseFlipped = int(suitcaseFlipped)
                stdio.write(SAY_SUITCASE_FLIPPED %
                            (1, suitcaseFlipped, player1Airport))
                assignAirportCanFlip(player1Airport)[suitcaseFlipped-1] = False
                print_single_suitcase_number(
                    assignAirport(player1Airport)[suitcaseFlipped-1])
                if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                    stdio.write(SAY_COLLECTED %
                                (1, suitcaseFlipped, player1Airport))
                    modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                    player1Suitcase += 1
                    assignAirportCanFlip(player1Airport)[0] = True
                    assignAirportCanFlip(player1Airport)[1] = True
                    assignAirportCanFlip(player1Airport)[2] = True
                    assignAirportCanFlip(player1Airport)[3] = True
                    if player1Suitcase == 10:
                        print_suitcase_grid(player1Suitcase, player2Suitcase)
                        stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                        stdio.write(WIN_MESSAGE % (1))
                        stdio.writeln(ASK_NEW_GAME)
                        if stdio.isEmpty():
                            termination(ERR_EMPTY_STD_INPUT)
                        newGame = stdio.readString()
                        if newGame == "Q":
                            termination(MSG_USER_TERMINATION)
                        if newGame == "Y":
                            stdio.writeln(SAY_YES_NEW_GAME)
                            game()
                        else:
                            termination(MSG_NO_NEW_GAME_TERMINATION)
                else:
                    stdio.write(SAY_NOT_COLLECTED %
                                (1, suitcaseFlipped, player1Airport))
                print_suitcase_grid(player1Suitcase, player2Suitcase)
                playerResponse = show_options(currentPlayer, False, False, usedRedDiskP2,
                                         player2Balance, costMatrix, game_mode, player1Airport, player2Airport)
                if playerResponse == "A":
                    termination(ERR_CANT_ASK)
            elif playerAnswer == "N":
                stdio.write(SAY_REFUSED_TO_LEAVE % (1, 2))
                response = show_options(1, False, True, usedRedDiskP2, player2Balance,
                                        costMatrix, game_mode, player1Airport, player2Airport)
                if response == "S":
                    if (assignAirportCanFlip(player2Airport)[0] == False or assignAirportCollectedSuitcases(player2Airport)[0] == True) and (assignAirportCanFlip(player2Airport)[1] == False or assignAirportCollectedSuitcases(player2Airport)[1] == True) and (assignAirportCanFlip(player2Airport)[2] == False or assignAirportCollectedSuitcases(player2Airport)[2] == True) and (assignAirportCanFlip(player2Airport)[3] == False or assignAirportCollectedSuitcases(player2Airport)[3] == True):
                        termination(ERR_CANT_STAY)
                    print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                        player2Airport), assignAirportCanFlip(player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (2, suitcaseFlipped, player2Airport))
                    assignAirportCanFlip(player2Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player2Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                        modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                        player2Suitcase += 1
                        assignAirportCanFlip(player2Airport)[0] = True
                        assignAirportCanFlip(player2Airport)[1] = True
                        assignAirportCanFlip(player2Airport)[2] = True
                        assignAirportCanFlip(player2Airport)[3] = True
                        if player2Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (2))
                            stdio.write(WIN_MESSAGE % (2))
                            stdio.writeln(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                if response == "F":
                    assignAirportCanFlip(player2Airport)[0] = True
                    assignAirportCanFlip(player2Airport)[1] = True
                    assignAirportCanFlip(player2Airport)[2] = True
                    assignAirportCanFlip(player2Airport)[3] = True
                    stdio.write(ASK_AIRPORT_DESTINATION % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    ap = stdio.readString()
                    if ap == "Q":
                        termination(MSG_USER_TERMINATION)
                    if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                        termination(ERR_INVALID_AIRPORT)
                    if ap == player2Airport:
                        termination(ERR_FLYING_TO_SAME_AIRPORT)
                    if ap == player1Airport:
                        termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                    flightCost = costMatrix[int(char_to_int(
                        player2Airport))][int(char_to_int(ap))]
                    if flightCost > player2Balance:
                        termination(ERR_BALANCE)
                    stdio.writen(SAY_FLIGHT_INFO %
                                 (2, player2Airport, ap, flightCost))
                    player2Airport = ap
                    player2Balance = player2Balance - flightCost
                    print_airport_grid(char_to_int(
                        player1Airport), char_to_int(player2Airport))
                    print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                        player2Airport), assignAirportCanFlip(player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (2, suitcaseFlipped, player2Airport))
                    assignAirportCanFlip(player2Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player2Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                        modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                        player2Suitcase += 1
                        assignAirportCanFlip(player2Airport)[0] = True
                        assignAirportCanFlip(player2Airport)[1] = True
                        assignAirportCanFlip(player2Airport)[2] = True
                        assignAirportCanFlip(player2Airport)[3] = True
                        if player2Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (2))
                            stdio.write(WIN_MESSAGE % (2))
                            stdio.writeln(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (2, suitcaseFlipped, player2Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                if response == "U":
                    if usedRedDiskP2 == True:
                        termination(ERR_NO_DISKS)
                    stdio.write(ASK_WHICH_OBSTACLE_DISK % (2))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    choice = stdio.readString()
                    if choice == "Q":
                        termination(MSG_USER_TERMINATION)
                    if choice not in ('R', 'G', 'Y', 'C', 'B', 'M'):
                        termination(ERR_INVALID_DISK)
                    if choice != "R":
                        termination(ERR_UNIMPLEMENTED)
                    usedRedDiskP2 = True
                    # change this for 2nd hand in
                    stdio.write(SAY_PLAY_OBSTACLE_DISK %
                                (2, OBSTACLE_DISK_STRINGS[RED_DISK]))
                    stdio.write(SAY_RED_DISK % (1, 2))
                    stdio.write(ASK_AIRPORT_DESTINATION % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    ap = stdio.readString()
                    if ap == "Q":
                        termination(MSG_USER_TERMINATION)
                    if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                        termination(ERR_INVALID_AIRPORT)
                    if ap == player1Airport:
                        termination(ERR_FLYING_TO_SAME_AIRPORT)
                    if ap == player2Airport:
                        termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
                    flightCost = costMatrix[int(char_to_int(
                        player1Airport))][int(char_to_int(ap))]
                    if flightCost > player2Balance:
                        termination(ERR_BALANCE)
                    stdio.write(SAY_FLIGHT_INFO % (1, player1Airport, ap, 0))
                    player1Airport = ap
                    player2Balance = player2Balance - flightCost

                    print_airport_grid(char_to_int(
                        player1Airport), char_to_int(player2Airport))
                    print_airport_suitcases(assignAirport(player1Airport), assignAirportCollectedSuitcases(
                        player1Airport), assignAirportCanFlip(player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(ASK_SUITCASE_POSITION % (1))
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    suitcaseFlipped = stdio.readString()
                    if suitcaseFlipped == "Q":
                        termination(MSG_USER_TERMINATION)
                    if suitcaseFlipped not in ("1", "2", "3", "4"):
                        termination(ERR_INVALID_SUITCASE_POSITION)
                    suitcaseFlipped = int(suitcaseFlipped)
                    stdio.write(SAY_SUITCASE_FLIPPED %
                                (1, suitcaseFlipped, player1Airport))
                    assignAirportCanFlip(player1Airport)[
                        suitcaseFlipped-1] = False
                    print_single_suitcase_number(
                        assignAirport(player1Airport)[suitcaseFlipped-1])
                    if int(assignAirport(player1Airport)[suitcaseFlipped-1]) - 1 == player1Suitcase:
                        stdio.write(SAY_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                        modifySuitcaseFlipped(player1Airport, suitcaseFlipped)
                        player1Suitcase += 1
                        assignAirportCanFlip(player1Airport)[0] = True
                        assignAirportCanFlip(player1Airport)[1] = True
                        assignAirportCanFlip(player1Airport)[2] = True
                        assignAirportCanFlip(player1Airport)[3] = True
                        if player1Suitcase == 10:
                            print_suitcase_grid(
                                player1Suitcase, player2Suitcase)
                            stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                            stdio.write(WIN_MESSAGE % (1))
                            stdio.writeln(ASK_NEW_GAME)
                            if stdio.isEmpty():
                                termination(ERR_EMPTY_STD_INPUT)
                            newGame = stdio.readString()
                            if newGame == "Q":
                                termination(MSG_USER_TERMINATION)
                            if newGame == "Y":
                                stdio.writeln(SAY_YES_NEW_GAME)
                                game()
                            else:
                                termination(MSG_NO_NEW_GAME_TERMINATION)
                    else:
                        stdio.write(SAY_NOT_COLLECTED %
                                    (1, suitcaseFlipped, player1Airport))
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(SAY_RED_DISK_DEDUCTION %
                                (2, 1, flightCost, player2Balance))
                    playerResponse = show_options(currentPlayer, False, False, usedRedDiskP2,
                                             player2Balance, costMatrix, game_mode, player1Airport, player2Airport)

        if playerResponse == "S":
            if (assignAirportCanFlip(player2Airport)[0] == False or assignAirportCollectedSuitcases(player2Airport)[0] == True) and (assignAirportCanFlip(player2Airport)[1] == False or assignAirportCollectedSuitcases(player2Airport)[1] == True) and (assignAirportCanFlip(player2Airport)[2] == False or assignAirportCollectedSuitcases(player2Airport)[2] == True) and (assignAirportCanFlip(player2Airport)[3] == False or assignAirportCollectedSuitcases(player2Airport)[3] == True):
                termination(ERR_CANT_STAY)
            print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                player2Airport), assignAirportCanFlip(player2Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)
            stdio.write(ASK_SUITCASE_POSITION % (2))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            suitcaseFlipped = stdio.readString()
            if suitcaseFlipped == "Q":
                termination(MSG_USER_TERMINATION)
            if suitcaseFlipped not in ("1", "2", "3", "4"):
                termination(ERR_INVALID_SUITCASE_POSITION)
            suitcaseFlipped = int(suitcaseFlipped)
            stdio.write(SAY_SUITCASE_FLIPPED %
                        (2, suitcaseFlipped, player2Airport))
            assignAirportCanFlip(player2Airport)[suitcaseFlipped-1] = False
            print_single_suitcase_number(
                assignAirport(player2Airport)[suitcaseFlipped-1])
            if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                stdio.write(SAY_COLLECTED %
                            (2, suitcaseFlipped, player2Airport))
                modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                player2Suitcase += 1
                assignAirportCanFlip(player2Airport)[0] = True
                assignAirportCanFlip(player2Airport)[1] = True
                assignAirportCanFlip(player2Airport)[2] = True
                assignAirportCanFlip(player2Airport)[3] = True
                if player1Suitcase == 10:
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(WIN_COLLECTED_ALL_SUITCASES % (1))
                    stdio.write(WIN_MESSAGE % (1))
                    stdio.writeln(ASK_NEW_GAME)
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    newGame = stdio.readString()
                    if newGame == "Q":
                        termination(MSG_USER_TERMINATION)
                    if newGame == "Y":
                        stdio.writeln(SAY_YES_NEW_GAME)
                        game()
                    else:
                        termination(MSG_NO_NEW_GAME_TERMINATION)
            else:
                stdio.write(SAY_NOT_COLLECTED %
                            (2, suitcaseFlipped, player2Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)

        if playerResponse == "F":
            assignAirportCanFlip(player2Airport)[0] = True
            assignAirportCanFlip(player2Airport)[1] = True
            assignAirportCanFlip(player2Airport)[2] = True
            assignAirportCanFlip(player2Airport)[3] = True
            stdio.write(ASK_AIRPORT_DESTINATION % (2))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            ap = stdio.readString()
            if ap == "Q":
                termination(MSG_USER_TERMINATION)
            if ap not in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
                termination(ERR_INVALID_AIRPORT)
            if ap == player2Airport:
                termination(ERR_FLYING_TO_SAME_AIRPORT)
            if ap == player1Airport:
                termination(ERR_FLYING_TO_OPPONENT_AIRPORT)
            flightCost = costMatrix[int(char_to_int(
                player2Airport))][int(char_to_int(ap))]
            if flightCost > player2Balance:
                termination(ERR_BALANCE)
            stdio.write(SAY_FLIGHT_INFO % (2, player2Airport, ap, flightCost))
            player2Airport = ap
            player2Balance = player2Balance - flightCost
            print_airport_grid(char_to_int(player1Airport),
                               char_to_int(player2Airport))
            print_airport_suitcases(assignAirport(player2Airport), assignAirportCollectedSuitcases(
                player2Airport), assignAirportCanFlip(player2Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)
            stdio.write(ASK_SUITCASE_POSITION % (2))
            if stdio.isEmpty():
                termination(ERR_EMPTY_STD_INPUT)
            suitcaseFlipped = stdio.readString()
            if suitcaseFlipped == "Q":
                termination(MSG_USER_TERMINATION)
            if suitcaseFlipped not in ("1", "2", "3", "4"):
                termination(ERR_INVALID_SUITCASE_POSITION)
            suitcaseFlipped = int(suitcaseFlipped)
            stdio.write(SAY_SUITCASE_FLIPPED %
                        (2, suitcaseFlipped, player2Airport))
            assignAirportCanFlip(player2Airport)[suitcaseFlipped-1] = False
            print_single_suitcase_number(
                assignAirport(player2Airport)[suitcaseFlipped-1])
            if int(assignAirport(player2Airport)[suitcaseFlipped-1]) - 1 == player2Suitcase:
                stdio.write(SAY_COLLECTED %
                            (2, suitcaseFlipped, player2Airport))
                modifySuitcaseFlipped(player2Airport, suitcaseFlipped)
                player2Suitcase += 1
                assignAirportCanFlip(player2Airport)[0] = True
                assignAirportCanFlip(player2Airport)[1] = True
                assignAirportCanFlip(player2Airport)[2] = True
                assignAirportCanFlip(player2Airport)[3] = True
                if player2Suitcase == 10:
                    print_suitcase_grid(player1Suitcase, player2Suitcase)
                    stdio.write(WIN_COLLECTED_ALL_SUITCASES % (2))
                    stdio.write(WIN_MESSAGE % (2))
                    stdio.writeln(ASK_NEW_GAME)
                    if stdio.isEmpty():
                        termination(ERR_EMPTY_STD_INPUT)
                    newGame = stdio.readString()
                    if newGame == "Q":
                        termination(MSG_USER_TERMINATION)
                    if newGame == "Y":
                        stdio.writeln(SAY_YES_NEW_GAME)
                        game()
                    else:
                        termination(MSG_NO_NEW_GAME_TERMINATION)
            else:
                stdio.write(SAY_NOT_COLLECTED %
                            (2, suitcaseFlipped, player2Airport))
            print_suitcase_grid(player1Suitcase, player2Suitcase)

        currentRound += 1 # increases the current round count as both players have taken their turn
        currentPlayer = currentPlayer - 1 #decreases current player as its now player 1's turn again


def termination(msg):
    stdio.writef('Termination: %s', str(msg))
    sys.exit(0)


def print_obstacle_disks(can_play_disk_array):
    """
    Print the obstacle disks available to the given player.

    NOTE: The Red disk should only be displayed here after the player has asked their opponent to leave their airport, and the opponent has refused to leave -- assuming they have not used it previously. In the case where it is possible to display the red disk, no other obstacle disks should be displayed, even if they have not been played yet. In the case where the player did not ask their opponent to leave their airport, only the non-red obstacle disks should be displayed (noting that, for the first hand-in, the non-red obstacle disks will never be available).

    Parameters
    ----------
    player
        the index of the current player. `0` for `P1` and `1` for `P2`.
    can_play_disk_array
        an array of six Booleans (`True` or `False`) corresponding to whether or not the disk at that index can be played or not.
        NOTE: the order of the array elements are important: `[can_play_red, can_play_green, can_play_yellow, can_play_cyan, can_play_black, can_play_magenta]`. When it is possible for can_play_red to be `True`, the others should be false, even if the player has not played any of the non-red disks yet. Similarly, when the other values can possibly be `True`, the red disk should not be `True`, even if the player has not played their red obstacle disk yet since the red obstacle disk can only and is the only obstacle disk that can played immediately after the current player has asked their opponent to leave their airport, and the opponent has refused to do so.
    """
    if game_over:
        return
    middle = ' x%11sx '
    outer1 = '     x x x     '
    outer2 = '  x         x  '
    colour_characters_array = ['R', 'G', 'Y', 'C', 'B', 'M']
    for row in range(7):
        for disk in range(len(colour_characters_array)):
            if disk == 0:
                stdio.write('\t')
            if not can_play_disk_array[disk]:
                continue
            if row == 0 or row == 6:
                stdio.write(outer1)
            elif row == 1 or row == 5:
                stdio.write(outer2)
            elif row == 2 or row == 4:
                stdio.writef(middle, ' ')
            else:
                stdio.writef(middle, colour_characters_array[disk].center(10))
        stdio.writeln()


def black_disk_print(suitcase_numbers_array, collected_array):
    """
    This function reveals the numbers behind the suitcases at their current airport. It also shows which of these suitcases have already been collected by either player.

    This function must only be called after a player correctly plays their black card. ''Correcly'', here, implies that you still have to perform logical checks to see whether the player is allowed to play their black card before calling this function.

    Parameters
    ----------
    suitcase_numbers_array
        A one-dimensional array with four elements. The elements are integer values -- the (usually hidden) numbers of each corresponding suitcase index. The array must contain four integer values, each between 1 and 10. These are the numbers the player needs to collect in sequence. The index of each number in the array corresponds to the index of the corresponding suitcase at the aiport.
    collected_array
        A one-dimensional array with four elements. The elements are boolean values, indicating whether or not a suitcase has already been collected by either player. If a suitcase at index `x` has been collected by either player, the value of `collected_array[x]` will be `True`. In contrast, if the suitcase at index `x` has not yet been collected, the value of `collected_array[x]` will be `False`.
        This variable is used to decide whether a cross should be drawn through the card. If the suitcase has been collected, a cross is drawn through the card and the number corresponding to that suitcase is displayed in the middle of the card. If the suitcase has not been collected, the number is displayed in the middle of the card, but no cross is drawn through the card.
        The index of each Boolean in the array corresponds to the index of the corresponding suitcase at the aiport.
    """
    if game_over:
        return
    space = ' '*5
    card_edge = '%5s' + CORN + LINE * 7 + CORN
    inside = space + WALL + '%-7s' + WALL
    empty = ' '*7
    uncollected = [empty, empty, ' ' * 3, empty, empty]
    taken1 = 'x     x'
    taken2 = ' x   x '
    collected = [taken1, taken2, ' ' * 3, taken2, taken1]

    for card_pos in range(SUITCASES_PER_AIRPORT):
        stdio.writef(card_edge, space)
    stdio.writeln()

    for i in range(5):
        for card_pos in range(SUITCASES_PER_AIRPORT):
            val = str(suitcase_numbers_array[card_pos]) if i == 2 else ''
            if collected_array[card_pos]:
                stdio.writef(inside, collected[i] + val)
            else:
                stdio.writef(inside, uncollected[i] + val)
        stdio.writeln()

    for card_pos in range(SUITCASES_PER_AIRPORT):
        stdio.writef(card_edge, str(card_pos+1) + '. ')
    stdio.writeln('\n')


def print_single_suitcase_number(number):
    # Do not use this function to display suitcase numbers when a black obstacle disk is played. Use the `black_disk_print()` function instead.
    if game_over:
        return
    card_edge = CORN + LINE * 7 + CORN
    middle = WALL + '%7s' + WALL + '\n'
    blank = ' '*7
    card_number = str(number).center(7)
    stdio.writeln(card_edge)
    for i in range(5):
        stdio.writef(middle, card_number if i == 2 else blank)
    stdio.writeln(card_edge + '\n')


def print_airport_suitcases(suitcase_numbers_array, collected_array, allowed_to_flip_array):
    if game_over:
        return
    space = ' '*5
    card_edge = '%5s' + CORN + LINE * 7 + CORN
    inside = space + WALL + '%-7s' + WALL
    empty = ' '*7
    unflipped = ['   _   ', ' xX Xx ', ' x   x ', ' xXXXx ', empty]
    taken1 = 'x     x'
    taken2 = ' x   x '
    collected = [taken1, taken2, ' ' * 3, taken2, taken1]
    stdio.writeln('Suitcases at the current airport:')

    for card_pos in range(SUITCASES_PER_AIRPORT):
        if allowed_to_flip_array[card_pos]:
            stdio.writef(card_edge, space)
    stdio.writeln()

    for i in range(5):
        for card_pos in range(SUITCASES_PER_AIRPORT):
            if not allowed_to_flip_array[card_pos]:
                continue
            if collected_array[card_pos]:
                val = str(suitcase_numbers_array[card_pos]) if i == 2 else ''
                stdio.writef(inside, collected[i] + val)
            else:
                stdio.writef(inside, unflipped[i])
        stdio.writeln()

    for card_pos in range(SUITCASES_PER_AIRPORT):
        if allowed_to_flip_array[card_pos]:
            stdio.writef(card_edge, str(card_pos+1) + '. ')
    stdio.writeln('\n')


def write_center(text, length=5):
    stdio.writef(' %s |', text.center(length))


def write_center(text, length=5):
    stdio.writef(' %s |', text.center(length))


def print_cost_matrix(flight_cost_matrix, cur_player, cur_player_wallet, cur_round_number):
    if game_over:
        return
    header_line = WALL + ' %-28s%s%28s ' + WALL
    stdio.writeln(CORN + LINE * (87) + CORN)
    round_info = f'Round {cur_round_number}'
    player_info = f'Player {cur_player + 1}'.center(29)
    wallet_info = f'Balance: R{float(cur_player_wallet):.2f}'
    stdio.writef(header_line, round_info, player_info, wallet_info)
    edge = '\n' + CORN + (LINE * 7 + CORN) * 11
    stdio.writeln(edge)
    stdio.writef('%s', WALL)
    write_center(' ', length=5)
    for col in range(AIRPORTS):
        write_center(int_to_char(col))
    stdio.writeln(edge)
    for row in range(AIRPORTS):
        stdio.writef('%s', WALL)
        write_center(int_to_char(row), length=5)
        for col in range(AIRPORTS):
            write_center(f'{float(flight_cost_matrix[row][col]):.2f}')
        stdio.writeln()
    stdio.writeln(edge[1:] + '\n')


def print_suitcase_grid(p1_last_suitecase, p2_last_suitecase):
    header = 'Player Suitcases'
    generic_grid_print(header, p1_last_suitecase,
                       p2_last_suitecase, True, False)


def print_airport_grid(p1_airport_id, p2_airport_id):
    header = 'Airplane Locations'
    generic_grid_print(header, p1_airport_id, p2_airport_id, False, True)


def generic_grid_print(header_text, p1_position, p2_position, seperate_players, use_letters):
    if game_over:
        return
    p1 = 'P1'
    p2 = 'P2'
    player_indicator = ' %2s' + ' '*5 + '%2s ' + WALL
    centre_indicator = ' '*5 + '%-2s' + ' '*4 + WALL
    seperator = CORN + (LINE * 11 + CORN) * 5
    stdio.writeln(CORN + LINE * (12 * 5 - 1) + CORN)
    stdio.writef('%s%s%s\n', WALL, header_text.center(
        len(seperator) - 2), WALL)
    for row in range(2):
        stdio.writef('%s\n', seperator)
        for i in range(5):
            stdio.write(WALL)
            for col in range(5):
                cell = row * 5 + col
                if i == 2:
                    stdio.writef(centre_indicator, int_to_char(
                        cell) if use_letters else cell + 1)
                elif seperate_players and i == 0:
                    stdio.writef(player_indicator, p1 if cell+1 ==
                                 p1_position else ' ', p2 if cell+1 == p2_position else ' ')
                elif seperate_players and i == 4:
                    stdio.writef(player_indicator, p2 if cell+1 ==
                                 p2_position else ' ', p1 if cell+1 == p1_position else ' ')
                elif cell == p1_position and (i == 0 or i == 4):
                    stdio.writef(player_indicator, p1, p1)
                elif cell == p2_position and (i == 0 or i == 4):
                    stdio.writef(player_indicator, p2, p2)
                else:
                    stdio.writef(centre_indicator, ' ')
            stdio.write('\n')
    stdio.writef('%s\n\n', seperator)


def print_command_line_args(game_mode_val, graphics_mode_val):
    stdio.writef('Game mode: %d\nGraphics mode: %d\n\n',
                 game_mode_val, graphics_mode_val)


if __name__ == '__main__':
    runner()
