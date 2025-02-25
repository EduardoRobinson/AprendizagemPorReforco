from maspy import *
from maspy.learning import *


class SortingBox(Environment):
    def __init__(self,env_name=None):
        super().__init__(env_name)
        self.create(Percept("Object_1",("Shelf","Box_1","Box_2","Box_3"),listed))
        self.create(Percept("Object_2",("Shelf","Box_1","Box_2","Box_3"),listed))
        self.possible_starts={"Object_1":"Shelf","Object_2":"Shelf"}

    def move_transition(self,state:dict,obj_to_box:tuple[str,str]):
        obj, box = obj_to_box
        obj_state:str = state[obj]
        if obj_state == "Shelf":
            state[obj] = box
            if(obj=="Object_1"):
                if box == "Box_1":
                    reward = 5
                if box == "Box_2":
                    reward = -5
                if box == "Box_3":
                    reward = 7           
            elif(obj=="Object_2"):
                if box == "Box_1":
                    reward = -5
                if box == "Box_2":
                    reward = 5
                if box == "Box_3":
                    reward = -2
        else:
            reward = -5
        terminated = False
        for value in state.values():
            if value != "Shelf":
                continue
            break
        else:
            terminated = True
            
        return state,reward,terminated



    #@action(listed,(('Object_1','Box_1'),('Object_1','Box_2'),('Object_1','Box_3'),('Object_2','Box_1'),('Object_2','Box_2'),('Object_2','Box_3')),move_transition)
    @action(cartesian,(('Object_1','Object_2'),('Box_1','Box_2','Box_3')),move_transition)
    def move(self,agt,obj_to_box:tuple[str,str]):
        obj,box=obj_to_box
        objeto= self.get(Percept(obj,Any))
        assert isinstance(objeto,Percept)
        self.print(f"{agt} is moving {obj} from {objeto.args} to {box}")
        self.change(objeto,box)




class BoxAgent(Agent):
    @pl(gain,Goal("make_model",Any))
    def makeModel(self,src,model_list:list[EnvModel]):
        model = model_list[0]
        print(f'actions:{model.action_space} space:{model.observation_space}')
        model.learn(qlearning,num_episodes=100)
        ag.auto_action = True
        ag.add_policy(model)







if __name__== "__main__":
    env = SortingBox()
    model = EnvModel(env)
    ag = BoxAgent()
    ag.add(Goal("make_model",[model]))
    Admin().start_system()

