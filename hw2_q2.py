from collections import namedtuple
from enum import Enum

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """

    update_listing = [] # agents' updated condition
    sick_and_cure = [] # agents that will participate in a meeting

    for agent in agent_listing: 
        # add healthy and dead to the updated list w/o any change 
        if agent.category == Condition.HEALTHY or agent.category == Condition.DEAD: 
            update_listing.append(agent)
        else: 
            sick_and_cure.append(agent)

    # pairs for meetup
    paired_list = pair_up(sick_and_cure)

    #calculate the condition post meeting 
    for pair in paired_list:
        update_listing.append(post_meetup_condition(pair))
    
    return update_listing


# Helper Functions

def pair_up(agent_listing: tuple) -> list: 
    """Divide the list of agents to pairs. 
     
    If there's an uneven number of agents, the last agent will remain the same.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of couples of Agents - defining the meeting couple
       
          
    """
    paired_list = []
    for i in range (0, len(agent_listing), 2): 
        if i+1 < len(agent_listing):
            paired_list.append((agent_listing[i] , agent_listing[i+1]))
        else: # in case of odd number of agents, leave the lat one alone
            paired_list.append((agent_listing[i],))
    
    return paired_list


def get_better(agent):
    """decrease the condition of an agent by 1

    Parameters
    ----------
    agent : Agent - a single object with condition 

    Returns
    -------
    The agent with a better condition
    
    """
    new_val = agent.category.value - 1  
    return Agent(agent.name, Condition(new_val))


def get_worse(agent):
    """increase the condition of an agent by 1

    Parameters
    ----------
    agent : Agent - a single object with condition 

    Returns
    -------
    The agent with a worse condition
    
    """
    new_val = agent.category.value + 1  
    return Agent(agent.name, Condition(new_val))


def post_meetup_condition(pair: tuple) -> tuple:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    assumes the tuple is a pair (not a single agent)

    Parameters
    ----------
    pair : tuple of two agents and their condition

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    # if single return as is
    if len(pair) == 1:
            return pair
    
    # both are CURE → no change
    if all(agent.category == Condition.CURE for agent in pair):
        return pair  

    # one is CURE, help the other
    if any(agent.category == Condition.CURE for agent in pair):
        # only decrease the non-CURE agents
        updated = tuple(
            agent if agent.category == Condition.CURE else get_better(agent)
            for agent in pair
        )
        return updated

    # else: no one is CURE → increase both
    updated = tuple(
        get_worse(agent) for agent in pair
    )
    return updated