import TaskGen, Utils, Task, Configure
import Logs

def dblatex_build(task):
    env = task.env
    bld = task.generator.bld
    src = task.inputs[0]
    cmd = '{0} -T {1} -o {2}.pdf {3} {4}'.format(env['DBLATEX'], env['DBLATEX_STYLE'], src.bld_base(env), env['DBLATEX_FLAGS'], src.srcpath(env))
    Logs.debug('Executing "{0}"'.format(cmd))
    bld.exec_command(cmd)

dblatex_vardeps = ['DBLATEX', 'DBLATEX_FLAGS']
class dblatex_taskgen(TaskGen.task_gen):
    def __init__(self, *k, **kw):
        TaskGen.task_gen.__init__(self, *k, **kw)

@TaskGen.feature('docbook')
def apply_dblatex(self):
    self.source = getattr(self, 'input', None)
    Logs.debug('apply_dblatex, sources {0}'.format(self.source))
    for filename in self.to_list(self.source):
        Logs.debug('apply_dblatex for "{0}"'.format(filename))
        node = self.path.find_resource(filename)
        if not node: raise Utils.WafError('Cannot find file "{0}"'.format(filename))
        task = self.create_task('dblatex', node, node.change_ext('.pdf'))
        task.env = self.env
        task.env['DBLATEX_STYLE'] = getattr(self, 'style', 'simple')
        task.curdirnode = self.path

@Configure.conftest
def detect(conf):
    env = conf.env
    conf.find_program('dblatex', var = 'dblatex'.upper())
    env['dblatex'.upper()+'_FLAGS'] = ''

b = Task.simple_task_type
b('dblatex', '${DBLATEX} -T ${DBLATEX_STYLE} ${DBLATEX_FLAGS} ${SRC} -o ${TGT}', color='BLUE', shell=False)
b = Task.task_type_from_func
cls = b('dblatex', dblatex_build, vars=dblatex_vardeps)

