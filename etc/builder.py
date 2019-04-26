from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, NDFileTemplate, makeTemplateInstance, includesTemplates
from iocbuilder.arginfo import *
from iocbuilder import Substitution, AutoSubstitution, SetSimulation, Device, records, Architecture, IocDataStream
from iocbuilder.modules.asyn import Asyn, AsynPort, AsynIP

@includesTemplates(NDFileTemplate)
class mar345Template(AutoSubstitution):
    TemplateFile = "mar345.template"
    #SubstitutionOverwrites = [_NDFile]

class mar345(AsynPort):
    """Creates a mar345 areaDetector driver"""
    Dependencies = (ADCore,)
    _SpecificTemplate = mar345Template
    def __init__(self, PORT = "mar1.cam", MARSERVER = "localhost:5001", BUFFERS = 50, MEMORY = 0, **args):
        # Make an asyn IP port to talk to mar345dtb on                                                                                     
        MARSERVER_PORT = PORT + "ip"
        self.ip = AsynIP(MARSERVER, name = MARSERVER_PORT,
            input_eos = "\n", output_eos = "\n")
        # Init the superclass                                                                                                              
        self.__super.__init__(PORT)
        # Init the file writing class                                                                                                      
        #self.file = _NDFile(**filter_dict(args, _NDFile.ArgInfo.Names()))
        # Store the args                                                                                                                   
        #self.__dict__.update(self.file.args)
        self.__dict__.update(locals())
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    # __init__ arguments                                                                                                                   
    # + _NDFile.ArgInfo
    ArgInfo = ADBaseTemplate.ArgInfo + NDFileTemplate.ArgInfo + \
            _SpecificTemplate.ArgInfo.filtered(without = ["MARSERVER_PORT"]) + \
            makeArgInfo(__init__,
        PORT = Simple('asyn port for mar345 detector'),
        MARSERVER = Simple('Machine:port that mar345dtb is running on', str),
        BUFFERS = Simple('Maximum number of NDArray buffers to be created for '
            'plugin callbacks', int),
        MEMORY = Simple('Max memory to allocate, should be maxw*maxh*nbuffer '
            'for driver and all attached plugins', int))

    # Device attributes                                                                                                                    
    LibFileList = ['mar345']
    DbdFileList = ['mar345Support']

    def Initialise(self):
        print '# mar345Config(portName, serverPort, maxBuffers, ' \
            'maxMemory)'
        print 'mar345Config("%(PORT)s", "%(MARSERVER_PORT)s", %(BUFFERS)d, ' \
            '%(MEMORY)d)' % self.__dict__
