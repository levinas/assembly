import glob
import logging
import os
import subprocess
from plugins import BaseAssembler
from yapsy.IPlugin import IPlugin

class A5Assembler(BaseAssembler, IPlugin):
    # TODO: update quast logic. For now output scaffolds as contigs.
    # OUTPUT = 'scaffolds'

    def run(self):
        """ 
        Build the command and run.
        Return list of contig file(s)
        """
        
        cmd_args = [os.path.join(os.getcwd(),self.executable)]
        libfile =  open(os.path.join(self.outpath, 'a5lib.out'), 'w')
        reads = self.data.readsets
        for d in reads:
            libfile.write('[LIB]\n')
            if d.type == 'paired':
                if len(d.files) == 1:
                    libfile.write('shuf={}\n'.format(d.files[0]))
                elif len(d.files) == 2:
                    libfile.write('p1={}\n'.format(d.files[0]))
                    libfile.write('p2={}\n'.format(d.files[1]))
            elif d.type == 'single':
                for up in d.files:
                    libfile.write('up={}\n'.format(up))
            try:
                assert d.insert is not None
                libfile.write('ins={}\n'.format(d['insert']))
            except:
                logging.info('No Insert Info Given')
        cmd_args.append(libfile.name)
        libfile.close()
        cmd_args.append('a5')
        self.arast_popen(cmd_args, cwd=self.outpath)

        contigs = glob.glob(self.outpath + '/*.contigs.fasta')
        scaffolds = glob.glob(self.outpath + '/*.final.scaffolds.fasta')

        output = {}
        if contigs:
            # output['contigs'] = contigs
            output['contigs'] = scaffolds
        if scaffolds:
            output['scaffolds'] = scaffolds

        return output

