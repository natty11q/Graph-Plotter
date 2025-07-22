import Common as Common # type: ignore noqa
import Utility.CoreUtility as Utility


# from ApplicationEngine.src.Core.Utility.Filemanager import * 


import time
from typing import Callable


class PlotEngineTime:

#------------- private:

    # inner class for timer
    class __Timer:
        def __init__(self, Duration : float, usesScaledTime : bool, endCall : Callable[[list [object]], None], endArgs : list [object], frameCall : Callable[[list [object]], None], frameArgs : list [object], callOnPhysicsThread : bool):
            self.__paused   : bool  = False
            self.__time     : float = 0
            self.__hasEnd   : bool  = (Duration >= 0)
            self.__Duration : float = Duration
            
            self.__Finished : bool = False
            
            self.__usesScaledTime : bool = usesScaledTime
            
            self.__endCall : Callable[[list], None] = endCall       # type: ignore
            self.__endArgs : list = endArgs                         # type: ignore
            
            self.__frameCall : Callable[[list], None] = frameCall   # type: ignore
            self.__frameArgs : list = frameArgs                     # type: ignore
            
            self.__isPhysTimer : bool = callOnPhysicsThread
        
        def Update(self, dt : float):
            self.__time += dt
            if self.__time > self.__Duration:
                self.__time = self.__Duration
            
            self.__OnUpdate()
        
        def __OnUpdate(self):
            self.__frameCall(*self.__frameArgs)       # type: ignore
        
        def __OnTermination(self):
            self.__endCall(*self.__endArgs)           # type: ignore

        def IsComplete(self):
            self.__Finished = bool((self.__Duration < self.__time) * self.__hasEnd) # unnecessary conversion , i know dw
            return self.__Finished



        def Terminate(self):
            self.__OnTermination
        
        def Increment(self, Deltatime : float, timeScale : float):
            if self.__usesScaledTime:
                self.__time += Deltatime
            else:
                self.__time += Deltatime * timeScale
            
            self.__Finished = bool((self.__Duration < self.__time) * self.__hasEnd)

        
        def Pause(self):
            self.__paused = True
        
        def UnPause(self):
            self.__paused = False
        
        def IsPaused(self):
            return self.__paused
        
        def IsPhysTimer(self):
            return self.__isPhysTimer
        
        def GetTime(self):
            return self.__time



#==================================================
    __TimeSettings = {} # used in LogicEngine
    __BASE_TIME_SCALE : float = __TimeSettings.get("BASE_TIME_SCALE",1)         # type: ignore
    __TimeScale : float = __BASE_TIME_SCALE
    
    __Deltatime : float = 0
    __ScaledDeltatime   : float  = 0
    
    __TotalElapsedTime  : float  = 0
    __ScaledElapsedTime : float  = 0
    
    
    __BASE_TICK_RATE : float = __TimeSettings.get("BASE_TICK_RATE",25)          # type: ignore
    __TickRate : float = __BASE_TICK_RATE
    
    
    __TickDelta : float = 0
    
    
    
    __TickCount : int = 0
    __FrameCount : int = 0
    
    __FPS : float = 0
    __FPS_CACHE : list [float] = [] # used to store the recent frame render times to find the current frame rate as an average
    __FPS_CACHE_SIZE : int = 120 # how many of the previous frames are we measuring

    

    __MAX_TIME_SCALE : float = 2 ** 32
    __MAX_TICK_RATE : float = 2 ** 32
    
    __MIN_TIME_SCALE : float = 0.0
    __MIN_TICK_RATE : float = 0.0
    
    
    __b_FRAMERATE_UNCAPPED = True
    __f_TARGET_FRAME_RATE : float = __TimeSettings.get("STARTING_TARGET_FRAMERATEE",120) # type: ignore
    __b_V_SYNC : bool = False

# init as this so that the first frame has a deltatime of 0 instead of a large number (due to time.time() - 0 on frame 1)
    __frameStart    : float  = time.perf_counter()
    __frameEnd      : float  = time.perf_counter()

    __tickStart    : float  = time.perf_counter()
    __tickEnd      : float  = time.perf_counter()
    
    # timers are handled with ids
    # Note :: Ids should never change until the function is complete
    __Timers : dict [int , __Timer] = {}

    __FRAME_SLEEP_ALLOWANCE = 0.0005 / 1000  # slight reduction in waiting time to get as close to target framerate as possible

#========================================================================
   
    @staticmethod
    def __UpdateTimers():
        """
            Update all the timers that arent bound to a physics thread
            IE : called every render frame
        """
        for timer in PlotEngineTime.__Timers.values():
            if not timer.IsPhysTimer():
                timer.Update(PlotEngineTime.__Deltatime)
    @staticmethod
    def __UpdatePhysicsTimers():
        for timer in PlotEngineTime.__Timers.values():
            if timer.IsPhysTimer():
                timer.Update(PlotEngineTime.__Deltatime)
    @staticmethod
    def __UpdateFPS():
        if len(PlotEngineTime.__FPS_CACHE) < PlotEngineTime.__FPS_CACHE_SIZE:
            PlotEngineTime.__FPS_CACHE.append(PlotEngineTime.__Deltatime)
        else:
            PlotEngineTime.__FPS = 1 / (sum(PlotEngineTime.__FPS_CACHE) / PlotEngineTime.__FPS_CACHE_SIZE) # caclulate average frames per second
            PlotEngineTime.__FPS_CACHE = []
            # print(f"fps : {LLEngineTime.FPS()}\n")
        
#--------------- public
    @staticmethod
    def TimeScale() -> float:
        return PlotEngineTime.__TimeScale
    
    @staticmethod
    def ScaledDeltaTime() -> float:
        return PlotEngineTime.__ScaledDeltatime
    
    @staticmethod
    def DeltaTime() -> float:
        return PlotEngineTime.__Deltatime
    
    @staticmethod
    def TickDelta() -> float:
        return PlotEngineTime.__TickDelta
    
    @staticmethod
    def Time() -> float:
        return PlotEngineTime.__TotalElapsedTime
    
    @staticmethod
    def ScaledTime() -> float:
        return PlotEngineTime.__ScaledElapsedTime
    
    @staticmethod
    def FPS() -> float:
        return PlotEngineTime.__FPS
    
    @staticmethod
    def FrameCount() -> int:
        return PlotEngineTime.__FrameCount
    
    @staticmethod
    def TickCount() -> int:
        return PlotEngineTime.__TickCount
    
    @staticmethod
    def TickRate() -> float:
        return PlotEngineTime.__BASE_TICK_RATE 
    
    @staticmethod
    def IsVsync() -> bool:
        return PlotEngineTime.__b_V_SYNC
    
    @staticmethod
    def TargetFrameRate() -> float:
        return PlotEngineTime.__f_TARGET_FRAME_RATE
    
    @staticmethod
    def SetTargetFramerate(framerate : float):
        if framerate > 0 + PlotEngineTime.__FRAME_SLEEP_ALLOWANCE:
            PlotEngineTime.__f_TARGET_FRAME_RATE = framerate
    
    ## TODO : add error handling or when an invalid value is input for the rates
    @staticmethod
    def SetTimeScale(scale : float) -> None:
        if scale < PlotEngineTime.__MAX_TIME_SCALE and scale > PlotEngineTime.__MIN_TIME_SCALE:
            PlotEngineTime.__TimeScale = scale
    
    @staticmethod
    def SetPhysicsTickRate(newRate : float) -> None:
        if newRate > PlotEngineTime.__MIN_TICK_RATE and newRate < PlotEngineTime.__MAX_TICK_RATE:
            PlotEngineTime.__TickRate = newRate
    
    @staticmethod    
    def SetVSync(VS : bool):
        PlotEngineTime.__b_V_SYNC = VS
    
    @staticmethod
    def UnCapFramerate():
        PlotEngineTime.__b_FRAMERATE_UNCAPPED = True
    
    @staticmethod
    def CapFramerate():
        PlotEngineTime.__b_FRAMERATE_UNCAPPED = False

    @staticmethod
    def CustomSleep() -> bool:
        """custom sleep funciton to ensure that the program can be quit safley even if sleeping"""
        #TODO : impl
        return False

    @staticmethod
    def Update() -> None:
        
        
        # restrict the frame rate
        PlotEngineTime.__frameEnd = time.perf_counter()
        
        if not PlotEngineTime.__b_FRAMERATE_UNCAPPED:
            TargetFrameTime = 1 / PlotEngineTime.__f_TARGET_FRAME_RATE
            elapsed_time = PlotEngineTime.__frameEnd - PlotEngineTime.__frameStart

            # Sleep only if necessary
            sleep_time = max(0, TargetFrameTime - elapsed_time - PlotEngineTime.__FRAME_SLEEP_ALLOWANCE)
            if sleep_time > 0:
                if sleep_time > 0.002:  # Sleep only if delay is large enough
                    time.sleep(sleep_time)
                else:
                    while time.perf_counter() - PlotEngineTime.__frameEnd < sleep_time:
                        pass  # Spin-wait for very short delays

        PlotEngineTime.__frameEnd = time.perf_counter()
        PlotEngineTime.__Deltatime        = PlotEngineTime.__frameEnd - PlotEngineTime.__frameStart
        PlotEngineTime.__ScaledDeltatime  = PlotEngineTime.__Deltatime * PlotEngineTime.__TimeScale
        PlotEngineTime.__TotalElapsedTime     += PlotEngineTime.__Deltatime
        PlotEngineTime.__ScaledElapsedTime    += PlotEngineTime.__ScaledDeltatime

        # print("1/dt : " , ( 1 / Time.__Deltatime) , "\n")
        # print("")


        
        
        PlotEngineTime.__UpdateFPS()
        PlotEngineTime.__UpdateTimers()
        
        PlotEngineTime.__frameStart = time.perf_counter()
    
    @staticmethod
    def PhysicsUpdate() -> None:
        # LLEngineTime.__TickDelta = 1/20
        # return 

        # restrict the frame rate
        PlotEngineTime.__tickEnd = time.perf_counter()
        
        # frameTime = Time.__frameEnd - Time.__frameStart
        TargetTickTime = 1 / PlotEngineTime.__TickRate
        elapsed_time = PlotEngineTime.__tickEnd - PlotEngineTime.__tickStart

        # WaitExit = False
        # while time.process_time() - LLEngineTime.__tickStart < (TargetTickTime - LLEngineTime.__FRAME_SLEEP_ALLOWANCE) and not WaitExit:
        #     WaitExit = LLEngineTime.CustomSleep()

        sleep_time = max(0, TargetTickTime - elapsed_time - PlotEngineTime.__FRAME_SLEEP_ALLOWANCE)
        if sleep_time > 0:
            time.sleep(sleep_time)

        PlotEngineTime.__tickEnd = time.perf_counter()
        PlotEngineTime.__TickDelta        = PlotEngineTime.__tickEnd - PlotEngineTime.__tickStart

        PlotEngineTime.__tickStart = time.perf_counter()

        PlotEngineTime.__UpdatePhysicsTimers()
    
    
    @staticmethod
    def StartTimerMs(duration : float = -1.0, usesScaledTime : bool = False, endCall : Callable[[list [object]], None] =  Utility.nullFunc, endArgs : list [object]= [], frameCall : Callable[[list[object]], None] = Utility.nullFunc, frameArgs : list[object]= [], callOnPhysicsThread : bool= False) -> int:
        """Creates a timer in milliseconds

        Args:
            duration (int, optional): the amount of time that the timer stays active (milliseconds). Defaults to -1 (does not terminate).
            usesScaledTime  (bool, optional)): determines wether the timer is affected by the current timeescale
            endCall (function, optional): called on the frame that the timer fginishes. Defaults to nullFunction.
            endArgs (list [any], optional): arguments passed to the function that calls when the timer ends.
            frameCall (function, optional): called every frame of the timer's lifetime. Defaults to nullFunction.
            frameArgs (list [any], optional): arguments passed to the function that calls each frame.
            callOnPhysicsThread (bool, optional): determines wether the timer is called on render frames or physics ticks. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        
        TimerID = Utility.FindLowestAvailableFreeInt(PlotEngineTime.__Timers) # type: ignore
        PlotEngineTime.__Timers[TimerID] = PlotEngineTime.__Timer(Duration= (duration / 1000), usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


    @staticmethod
    def StartTimerS(duration : float = -1.0, usesScaledTime : bool = False, endCall : Callable[[list [object]], None] =  Utility.nullFunc, endArgs : list [object]= [], frameCall : Callable[[list[object]], None] = Utility.nullFunc, frameArgs : list[object]= [], callOnPhysicsThread : bool= False) -> int:
        """Creates a timer in seconds

        Args:
            duration (int, optional): the amount of time that the timer stays active (milliseconds). Defaults to -1 (does not terminate).
            usesScaledTime  (bool, optional)): determines wether the timer is affected by the current timeescale
            endCall (function, optional): called on the frame that the timer fginishes. Defaults to nullFunction.
            endArgs (list [any], optional): arguments passed to the function that calls when the timer ends.
            frameCall (function, optional): called every frame of the timer's lifetime. Defaults to nullFunction.
            frameArgs (list [any], optional): arguments passed to the function that calls each frame.
            callOnPhysicsThread (bool, optional): determines wether the timer is called on render frames or physics ticks. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        
        TimerID = Utility.FindLowestAvailableFreeInt(PlotEngineTime.__Timers) # type: ignore
        PlotEngineTime.__Timers[TimerID] = PlotEngineTime.__Timer(Duration= duration, usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


#provide an interface for the timers
    
    @staticmethod
    def EndTimer(ID : int) -> None:
        if ID not in PlotEngineTime.__Timers.keys():
            return
        PlotEngineTime.__Timers[ID].Terminate()
        del PlotEngineTime.__Timers[ID]
    
    @staticmethod
    def PauseTimer(ID : int) -> None:
        if ID not in PlotEngineTime.__Timers.keys():
            return
        PlotEngineTime.__Timers[ID].Pause()
    
    @staticmethod
    def UnPauseTimer(ID : int) -> None:
        if ID not in PlotEngineTime.__Timers.keys():
            return
        PlotEngineTime.__Timers[ID].UnPause()

    @staticmethod    
    def IsTimerPaused(ID : int) -> None:
        if ID not in PlotEngineTime.__Timers.keys():
            return
        PlotEngineTime.__Timers[ID].IsPaused()

    @staticmethod    
    def GetTimerValue(ID : int) -> float:
        if ID not in PlotEngineTime.__Timers.keys():
            return -1.0 
        return PlotEngineTime.__Timers[ID].GetTime()

