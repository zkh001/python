
import subprocess
import re
import functools

class Command:
    def chainable(func):
        """ decorator """
        @functools.wraps(func)
        def _wrapper(self, *args, **kwargs):
            self.__pass_result( func(self, *args) )
            return self
    
        return _wrapper
        
    def __init__(self, results = []):
        """ usually unused """
        self.__results = results

    def get_results(self):
        """ call this finally to get results """
        return self.__results

    @staticmethod
    def execute(cmd_pieces):
        """ first executed method """
        p = subprocess.Popen(cmd_pieces, stdout=subprocess.PIPE)
        output = p.communicate()[0]
        return Command(output.rstrip("\n").split("\n") if output is not None else [''])

    @chainable
    def pipe(self, cmd_pieces):
        """ command pipe """
        dummy = subprocess.Popen(["echo", "\n".join(self.__results)], stdout = subprocess.PIPE)
        p = subprocess.Popen(cmd_pieces, stdin = dummy.stdout, stdout = subprocess.PIPE)
        output = p.communicate()[0]
        dummy.stdout.close()

        return output.rstrip("\n").split("\n") if output is not None else []

    @chainable
    def strip(self, rm_str = " "):
        return [ s.strip(rm_str) for s in self.__results ]

    @chainable
    def grep(self, regexp):
        return self.__filter(regexp, correct = True)

    @chainable
    def reject(self, regexp):
        return self.__filter(regexp, correct = False)

    @chainable
    def mapping(self, mapper):
        return map(mapper, self.__results)

    # ------------   private methods  --------------

    def __filter(self, regexp, correct = True):
        filtering = (lambda x:x is not None) if correct else (lambda x:x is None)

        filtered_list = []
        pat = re.compile(regexp)
        for l in self.__results:
            if filtering( pat.search(l) ):
                filtered_list.append(l)
        return filtered_list
        
    def __pass_result(self, results = []):
        self.__results = results
    


if __name__ == '__main__':
    # for debug
    
    # print( Command.execute(["ls", "-a"]).pipe(['grep', 'py']).get_result() )
    #print( Command.execute(["ls", "-a"]).pipe(['grep', 'py']).grep(r"ardrone").get_results() )

    a = Command.execute(["ls","-al"]).mapping( lambda x:x.translate(None, "py") )
    # print(a.get_results())

    for r in a.get_results():
        print(r)

