PSOATransRun 1.5 README                                                 2020-09-18


OVERVIEW

PSOATransRun is the reference implementation of the Positional-Slotted 
Object-Applicative RuleML (PSOA RuleML) language. This PSOATransRun release 
includes two translator compositions:

A translator PSOA2TPTP, from PSOA RuleML to a subset of the first-order logic 
language TPTP with a TPTP engine (here, the open source VampirePrime reasoner).

A translator PSOA2Prolog, from PSOA RuleML to a subset of the logic programming 
language ISO Prolog with one of the following well-known Prolog engines:
  XSB platform: The efficient XSB Prolog engine.
  SWI platform: The widespread SWI Prolog engine.

See http://psoa.ruleml.org for details of PSOA RuleML and PSOATransRun
and https://github.com/RuleML/PSOATransRunComponents for the Java/ANTLR/... sources
and http://psoa.ruleml.org/lib/ for the Prolog-targeting PSOA libraries.

In the following, we will focus on the PSOA2Prolog translator and engines.


REQUIREMENTS

Operating System: Windows, Linux, or Mac OS X
Prerequisites:
  Install Java version 8.0 or higher
  Install Prolog:
    XSB platform:
      Install (via http://xsb.sourceforge.net) XSB Prolog 3.6
      (from https://sourceforge.net/projects/xsb/files/xsb/3.6%20%28Gazpatcho%29/),
      rather than XSB 3.7 or 3.8,
      to a directory the path of which we will call <xsb_dir>, e.g. ...
      ... in Windows:                C:\Program Files\XSB
      ... in Linux / Mac OS X:       ~/XSB/
    SWI platform:
      Windows / Mac OS X:
        Install SWI Prolog from http://www.swi-prolog.org/download/stable,
        following the instructions, to the default installation directory. 
      Linux / Mac OS X:
        Linux users are encouraged to install SWI Prolog via their package
        manager (available in many distributions as swi-prolog or swipl), e.g.:
          sudo apt-get install swi-prolog
        Installation from source to /usr/local or a Homebrew installation (Mac OS X)
        is also supported.
      PSOATransRun will try to locate the SWI binary on all of the above default
      install locations. For custom install locations, the command line option 
      -x <swi_dir> must be specified, where <swi_dir> denotes the path of the 
      installation folder.


USAGE

Download http://psoa.ruleml.org/transrun/1.5/local/PSOATransRunLocal.jar to 
a directory, the path of which we will call <PSOATransRun_dir>
[e.g., in the directory above this README, right-click PSOATransRunLocal.jar,
click "Save Link As...", copy it to <PSOATransRun_dir>, possibly overwriting
any earlier version (no need for any other 'uninstall' action)]. 
Then follow these steps to use PSOATransRun (1. and 2. being just preparatory):

1. Open a window for a Command Prompt / Linux Terminal
Windows: start the Command Prompt (or PowerShell)
Linux:   start the Linux Terminal

2. Change the working directory to <PSOATransRun_dir> by executing
   cd <PSOATransRun_dir>
In Windows, if <PSOATransRun_dir> is on a different drive from the current
working directory, the command line option /d should be used:
   cd /d <PSOATransRun_dir>

3. Execute the following command to enter a basic query loop for a <kb_file>:

XSB platform: 
   
     java -jar PSOATransRunLocal.jar -x <xsb_dir> -i <kb_file>
   
  The -x <xsb_dir> part of the command can be omitted if the XSB_DIR environment
  variable is set to <xsb_dir>.

SWI platform:
  
     java -jar PSOATransRunLocal.jar -b swi -i <kb_file>
  
  If SWI is not installed to a default installation directory, you need to specify
  the path of its installation directory <swi_dir> by adding -x <swi_dir> to the above
  command (similarly as for XSB platform).
  
<kb_file> is the path of the input knowledge base (KB) file written in PSOA RuleML 
presentation syntax.

Here are copy&paste-ready examples of invoking the query loop command on different platforms,
assuming EDITME.psoa is a file, in <PSOATransRun_dir>, used for repeatedly editing KBs with
one's favorite text editor.

XSB platform:
  Windows [assuming the XSB installation directory <xsb_dir> is expanded to C:\Program Files\XSB]:
     java -jar PSOATransRunLocal.jar -x "C:\Program Files\XSB" -i EDITME.psoa
    
  Linux / Mac OS X [assuming the XSB installation directory <xsb_dir> is expanded to ~/XSB/]:
     java -jar PSOATransRunLocal.jar -x ~/XSB/ -i EDITME.psoa

SWI platform:
  Windows / Linux / Mac OS X [assuming the default install location of SWI Prolog (Windows / Mac OS X),
  an installation through a package manager, Homebrew (Linux, Mac OS X) or installation from
  source to /usr/local (Linux, Mac OS X)]:
     java -jar PSOATransRunLocal.jar -b swi -i EDITME.psoa
     
Advanced query loop variations will be shown via the help command (-?):
   java -jar PSOATransRunLocal.jar -?

4. After the message "KB loaded" is shown, queries can be posed. Each query must be 
written without intervening Newline characters and only terminated by pressing the Enter key.
One answer at a time will be shown. To get the next answer, press the semicolon key. 
To proceed to the next query, press the Enter key. To exit a query loop, press Ctrl+C, and
optionally change EDITME.psoa and go back to 3 (e.g., via the 'up-arrow' key on most platforms).


PSOATransRun 1.5 RELEASE NOTES
* Support syntactic recognition of "#"-prefixed embedded and top-level predicates to indicate oidless atoms
    [Raise error if whitespace follows hash ("#"), both for infix and prefix uses of "#"]
* For nested oidless atoms, add embedded objectification, complementing (top-level) objectification
* Introduce embedded "ground-fact-differentiated" objectification as
    differentiated objectification for ground facts
    undifferentiated objectification for everything else
* Examples can be found in
    http://wiki.ruleml.org/index.php/PSOA_RuleML#store-predicate
    http://wiki.ruleml.org/index.php/PSOA_RuleML#Presentation_Syntax_Long_and_Short_Forms
    https://github.com/RuleML/PSOATransRunComponents/blob/master/PSOATransRun/test-basic/embobj/ex_0/embobj_ex_0-KB.psoa
    https://github.com/RuleML/PSOATransRunComponents/blob/master/PSOATransRun/test-basic/embobj/store_franchise/store_franchise-KB.psoa
* Add support for C-style comment blocks, print deprecation warning for XML-style comment blocks
