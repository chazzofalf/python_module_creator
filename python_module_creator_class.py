import sys
class python_module_creator_callable_safe(object):    
    
    
    def call(self,name:str,dry_run:bool,pkg:bool):
        if dry_run:
            print('Performing Dry run')
        file_contents = self.__class_pattern.replace('{name}',name)
        
        if not pkg:
            file_contents = (self.__class_pattern + self.__class_pattern_part_main).replace('{name}',name)
            file_contents = file_contents.replace('{pkgprefix}','')
            file_contents = file_contents.replace('{suffix}','')
            if not dry_run:
                from io import FileIO
                from io import TextIOWrapper
                with  TextIOWrapper(FileIO(file=f'{name}.py',mode='w'),'utf8') as out:                                        
                    out.write(file_contents)                
                print(f'Wrote {name}.py')
            else:
                print(file_contents)
        else:
            file_contents = (self.__class_pattern).replace('{name}',name)            
            file_contents=file_contents.replace('{pkgprefix}',f'{name}/')
            file_contents=file_contents.replace('{suffix}','_inner')
            init_contents=self.__init_pattern.replace('{name}',name)
            init_contents=init_contents.replace('{suffix}','_inner')
            main_contents=self.__main_pattern.replace('{name}',name)
            if not dry_run:
                from io import FileIO
                from io import TextIOWrapper
                import os
                os.mkdir(name)
                with  TextIOWrapper(FileIO(file=f'{name}/{name}_inner.py',mode='w'),'utf8') as class_out:
                    with TextIOWrapper(FileIO(file=f'{name}/__main__.py',mode='w'),'utf8') as main_out:
                        with TextIOWrapper(FileIO(file=f'{name}/__init__.py',mode='w'),'utf8') as init_out:
                            class_out.write(file_contents)
                            main_out.write(main_contents)
                            init_out.write(init_contents)
            else:
                for f in [file_contents,init_contents,main_contents]:
                    print(f)
                
    def __init__(self) -> None:
        self.__main_pattern='''#!/bin/python
# {name}/__main__.py
import sys
import {name}
def main():
    # Handle Command Line Argument Here
    pass

if __name__=="__main__":
    main()
        '''
        self.__init_pattern='''#!/bin/python
# {name}/__init__.py
import sys
import {name}
import {name}.{name}{suffix}
sys.modules[__name__].__class__ = {name}.{name}{suffix}.{name}_callable
        '''
        self.__class_pattern='''#!/bin/python
# {pkgprefix}{name}{suffix}.py
import sys
class {name}_callable_safe(object):
    def __init__(self):
        # Do internal setup here.
        pass
    def call(self):
        # Add Code Here
        return None
class {name}_callable(sys.modules[__name__].__class__):
    def __init__(self):
        pass
    def __call__(self):
        obj={name}_callable_safe()
        return obj.call()'''
        self.__class_pattern_part_main='''
if __name__=="__main__":
    {name}_callable()()
else:
    sys.modules[__name__].__class__ = {name}_callable        
 '''       
    @property
    def pattern(self):
        return self.__class_pattern
class python_module_creator_callable(sys.modules[__name__].__class__):
    def __init__(self, name: str, doc: str | None = ...) -> None:
        super().__init__(name, doc)
    # def __init__(self):
        
    def __call__(self,name:str,dry_run:bool=False,pkg=False):
        obj=python_module_creator_callable_safe()
        obj.call(name=name,dry_run=dry_run,pkg=pkg)

if __name__=="__main__":    
    python_module_creator_callable()()
else:
    sys.modules[__name__].__class__ = python_module_creator_callable