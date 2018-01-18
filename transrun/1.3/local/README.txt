PSOATransRun 1.3 README                                              2018-01-18

OVERVIEW
PSOATransRun is the reference implementation of the Positional-Slotted Object-Applicative
RuleML (PSOA RuleML) language. This PSOATransRun release includes a composition 
of a translator PSOA2Prolog, from PSOA RuleML to a subset of the logic 
programming language ISO Prolog, with the well-known efficient XSB Prolog engine.
See http://psoa.ruleml.org for details of PSOA RuleML and PSOATransRun
and https://github.com/RuleML/PSOATransRunComponents for the repository.

REQUIREMENTS
Operating System: Windows, Linux, or Mac OS X
Prerequisites:
  Install Java version 8.0 or higher
  Install XSB Prolog 3.6 or higher (http://xsb.sourceforge.net) to a directory,
  the path of which we will call <xsb_dir>, e.g. ...
  ... in Windows:                C:\Program Files\XSB
  ... in Linux/Mac OS X:         ~/XSB/

USAGE
Download http://psoa.ruleml.org/transrun/1.3/local/PSOATransRunLocal.jar to 
a directory, the path of which we will call <PSOATransRun_dir>. 
Then follow these steps to use PSOATransRun (1. and 2. being just preparatory):

1. Open a window for a Command Prompt / Linux Terminal
Windows: see http://windows.microsoft.com/en-ca/windows-vista/open-a-command-prompt-window
Linux: start the Linux Terminal

2. Change the working directory to <PSOATransRun_dir> by executing
   cd <PSOATransRun_dir>
In Windows, if <PSOATransRun_dir> is on a different drive from the current
working directory, the command line option /d should be used:
   cd /d <PSOATransRun_dir>

3. Execute the following command to enter a basic query loop for a <kb_file>:

   java -jar PSOATransRunLocal.jar -x <xsb_dir> -i <kb_file>
   
The -x <xsb_dir> part of the command can be omitted if the XSB_DIR environment
variable is set to <xsb_dir>.
<kb_file> is the path of the input knowledge base (KB) file written in PSOA RuleML 
presentation syntax.

Here are copy&paste-ready examples of invoking the query loop command on different platforms,
assuming EDITME.psoa is a file, in <PSOATransRun_dir>, used for repeatedly editing KBs with
one's favorite text editor.

Windows (assuming the XSB installation directory <xsb_dir> is expanded to C:\Program Files\XSB):
   java -jar PSOATransRunLocal.jar -x "C:\Program Files\XSB" -i EDITME.psoa
    
Linux/Mac OS X (assuming the XSB installation directory <xsb_dir> is expanded to ~/XSB/):
   java -jar PSOATransRunLocal.jar -x ~/XSB/ -i EDITME.psoa

Advanced query loop variations will be shown via the help command (-?):
   java -jar PSOATransRunLocal.jar -?

4. After the message "KB loaded" is shown, queries can be posed. Each query must be 
written without intervening Newline characters and only terminated by pressing the Enter key.
One answer at a time will be shown. To get the next answer, press the semicolon key. 
To proceed to the next query, press the Enter key. To exit a query loop, press Ctrl+C, and
optionally change EDITME.psoa and go back to 3 (e.g., via the 'up-arrow' key on most platforms).

PSOATransRun 1.3 RELEASE NOTES
* Added support for dependent and independent descriptors, see https://arxiv.org/abs/1712.02869
* Added built-ins from ISO Prolog, see http://wiki.ruleml.org/index.php/PSOA_RuleML#Built-ins
