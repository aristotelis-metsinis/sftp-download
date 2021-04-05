#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    A script that connects and logs into a specified host at a predefined port with a given username, and password 
    and copies over "SFTP" all files from a remote source directory to a local destination directory.
    User can also choose to delete the remote files that have been already downloaded.

    Developed by Aristotelis Metsinis [ aristotelis.metsinis@gmail.com ] in June 2020 - version 1.0
    Comments and bug fixing in April 2021 - version 1.1
    
    Tested with Python 2.7.6 and 3.8.7
"""

# --------------------------------------------------------------------------------------------------

# The following "warning" was thrown during script's execution :
# 
#   /usr/local/lib/python2.7/dist-packages/cryptography/hazmat/primitives/constant_time.py:26:
#   CryptographyDeprecationWarning: Support for your Python version is deprecated. The next version of
#   cryptography will remove support. Please upgrade to a release (2.7.7+) that supports hmac.compare_digest
#   as soon as possible.
#	      utils.PersistentlyDeprecated2018,
#
# Issue "fixed" by adding the following lines of code :
#
# Warning Framework - Deliver non-fatal alerts to the user about issues encountered when running a program.
import warnings
# API for manipulating warning filters.
# The determination whether to issue a warning message is controlled by the "warnings" filter, which is a 
# sequence of matching rules and actions. Rules can be added to the filter by calling "filterwarnings()".
# The "warnings" filter controls whether warnings are ignored, displayed, or turned into errors (raising 
# an exception). Action = "ignore", never print matching warnings.
warnings.filterwarnings( 'ignore' )
#
# Provides cryptographic recipes and primitives.
# Includes both high level recipes and low level interfaces to common cryptographic algorithms.
import cryptography
from cryptography import utils
# Suppress "Cryptography" deprecation warning using the "catch_warnings" context manager.
with warnings.catch_warnings():
    warnings.simplefilter( 'ignore', cryptography.utils.CryptographyDeprecationWarning )
    # Module contains functions for operating with secret data in a way that does not leak information 
    # about that data through how long it takes to perform the operation.
    import cryptography.hazmat.primitives.constant_time
#

# Implements some useful functions on pathnames.
import os.path
# Provides access to some variables used or maintained by the interpreter and to functions that interact 
# strongly with the interpreter.
import sys
# A simple interface to "SFTP"; offers high level abstractions and task based routines to handle "SFTP" needs.
# Is just a thin wrapper over paramiko’s "SFTPClient".
import pysftp
# Parser for command-line options, arguments and sub-commands.
import argparse
# Logging facility; defines functions and classes, which implement a flexible event logging system for 
# applications and libraries.
import logging
# Logging handler that supports rotation of disk log files at certain timed intervals.
from logging.handlers import TimedRotatingFileHandler

# --------------------------------------------------------------------------------------------------

# Initialise the "SFTP" connection object.
connection = None 

# Disk log files will be saved under the following folder :
logs_folder = "logs"
# Disk log files will be created with the following name. The system will save old log files by 
# appending extensions to this filename.
logs_filename = "download.log"

# --------------------------------------------------------------------------------------------------

def sftp_connection( sftp_host, username, password, port ):
    """
        Instantiates a connection object, which is the base of "pysftp"
       
        Parameters
        ----------
            sftp_host : str 
                The Hostname or IP of the remote machine
            username  : str
                Username at the remote machine
            password  : str
                Password at the remote machine
            port      : str
                The SSH port of the remote machine
                
        Returns
        -------
            obj
                The connection to the requested host

        Raises
        ------
            Exception in case of error such as ConnectionException, CredentialException, 
            SSHException, AuthenticationException, PasswordRequiredException, HostKeysException
    """
    
    try:
        # Connect and log into the specified host at the input port with the given username, and password.
        sftp = pysftp.Connection( sftp_host, username=username, password=password, port=int( port ) )
    except Exception as e:
        # Raise exception in case of error.
        raise Exception( "Connecting to '%s:%s' : %s" % ( sftp_host, port, str( e ) ) )
    else:
        # Return the connection object to the requested host if no errors were raised.
        return sftp

# --------------------------------------------------------------------------------------------------

def list_remote_directory( remote_dir ):
    """
        Lists files that reside under a remote directory
        
        Parameters
        ----------
            remote_dir : str
                The remote directory

        Returns
        -------
            list
                The sorted list of remote files ordered by their (modification) date (descending order)
                
        Raises
        ------
            Exception in case of error such as IOError
    """
    
    try:
        # Change the current working directory on the remote machine to the given remote directory.
        connection.chdir( remote_dir )
        # Initially, a sorted list is being returned, instead of paramiko’s arbitrary order, of "SFTPAttribute" objects 
        # of the files/subdirectories that reside under the given remote directory. 
        # The list is sorted by "SFTPAttribute.filename". It does not include the special entries "." and "..". 
        # A "SFTPAttribute" object will contain the filename and also a "st_mtime" field (among others). Then, the list 
        # is being sorted on that "st_mtime" field to get the list of objects ordered by their (modification) 
        # date (descending order). And finally, we keep only the objects, which are files under that remote directory
        # and specifically the filenames associated with these files (if any).
        remote_files = [ x.filename for x in sorted( connection.listdir_attr(), key = lambda f : f.st_mtime, reverse=True ) if connection.isfile( x.filename ) ]
    except Exception as e:
        # Raise exception in case of error.
        raise Exception( "Listing remote directory '%s' : %s" % ( remote_dir, str( e ) ) )
    else:
        # Return the sorted list of remote files if no errors were raised.
        return remote_files
        
# --------------------------------------------------------------------------------------------------

def copy_remote_directory( remote_dir, local_dir ):
    """
        Copies all files from a remote directory to a local directory, preserving their modification time
        
        Parameters
        ----------
            remote_dir : str
                The remote directory to copy from (source)
            local_dir  : str
                The local directory to copy to (target)

        Returns
        -------
            None
            
        Raises
        ------
            Exception in case of error
    """
    
    try:
        # Copy all files that reside under the given remote directory to a local directory (non-recursive)
        # preserving the modification time on files.
        connection.get_d( remote_dir, local_dir, preserve_mtime=True )
    except Exception as e:
        # Raise exception in case of error.
        raise Exception( "Copying files of remote directory '%s' to local path '%s' : %s" % ( remote_dir, local_dir, str( e ) ) )

# --------------------------------------------------------------------------------------------------

def delete_remote_file( file ):
    """
        Deletes a remote file
        
        Parameters
        ----------
            file : str
                The remote file to delete

        Returns
        -------
            None
            
        Raises
        ------
            Exception in case of error such as IOError             
    """
    
    # If input "remote-path" is a file,
    if ( connection.isfile( file ) ):
        try:
            # Delete the remote file.
            connection.remove( file )
        except Exception as e:
            # Raise exception in case of error.
            raise Exception( "Deleting remote file '%s' : %s" % ( file, str( e ) ) )

# --------------------------------------------------------------------------------------------------
     
# Execute only if run as a script.
if __name__ == "__main__":

    # If the predefined log directory does not already exist then create a directory with the given name 
    # and numeric mode.
    if not os.path.exists( logs_folder ):
        os.mkdir( logs_folder, 0o755 )

    # Create a "root" logger, configure it, and return it :            
    # Return a logger, which is the "root" logger.
    log = logging.getLogger()
    # Set the threshold for this logger to the input level.
    log.setLevel( logging.INFO )
    #
    # Return a new instance of the "Formatter" class, initialized with a format string for the message as a whole.
    formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
    #
    # Return a new instance of the "StreamHandler" class, with the input stream used for logging output.
    console = logging.StreamHandler( sys.stdout )
    # Set the threshold for this handler to the input level.
    console.setLevel( logging.DEBUG )
    # Set the "Formatter" for this handler.
    console.setFormatter( formatter )
    # Add the specified handler to the "root" logger.
    log.addHandler( console )
    #
    # Support rotation of disk log files at certain timed intervals :
    # Return a new instance of the "TimedRotatingFileHandler" class. The specified file is opened and used as 
    # the stream for logging. On rotating it also sets the filename suffix, while the extensions are date-and-time based. 
    # Rotating happens based on the product of "when" and "interval". 
    # Roll over at "midnight" and at most "backupCount" files will be kept, the file will be opened with the specified encoding
    # and times in "UTC" will be used.
    rotating_file_handler = logging.handlers.TimedRotatingFileHandler( logs_folder + "/" + logs_filename, when='midnight', interval=1, backupCount=10, encoding="UTF-8", utc=True )
    # Set the threshold for this handler to input level.
    rotating_file_handler.setLevel( logging.DEBUG )
    # Set the "Formatter" for this handler.
    rotating_file_handler.setFormatter( formatter )
    # Add the specified handler to the "root" logger.
    log.addHandler( rotating_file_handler )

    # Create a new "ArgumentParser" object with the given text to display before the argument help.
    # The "ArgumentParser" object will hold all the information necessary to parse the command line into Python data types.
    arg = argparse.ArgumentParser( description="A script that connects and logs into a specified host at a predefined port with a given username, and password and copies over \"SFTP\" all files from a remote source directory to a local destination directory. User can also choose to delete the remote files that have been already downloaded." )
    # Fill the "ArgumentParser" object with information about program arguments, defining how a single command-line argument 
    # should be parsed, by specifying a list of option strings, whether or not the command-line option may be omitted, the 
    # basic type of action to be taken when this argument is encountered at the command line, a brief description of what the 
    # argument does, and the value produced if the argument is absent from the command line :
    arg.add_argument( '-H', '--host', required=True, action="store", help="hostname or IP address" )
    arg.add_argument( '-P', '--port', default=22, action="store", help="server port, default = 22" )
    arg.add_argument( '-s', '--source', action="store", required=True, help="remote directory to fetch files from" )
    arg.add_argument( '-d', '--destination', required=True, help="local folder to store fetched files to" )
    arg.add_argument( '-u', '--user', required=True, help="username for login" )
    arg.add_argument( '-p', '--password', required=True, help="password for login" )
    arg.add_argument( '--delete', default=False, action="store_true", help="delete remote files" )
    # Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace.
    args = arg.parse_args()

    try:
        # Log a message with level INFO on the "root" logger - print input remote host, port, and directory :
        log.info( "---------------------------------------------------------------------------------" )
        log.info( "Logging to remote server 'sftp://%s:%s%s'" % ( args.host, args.port, args.source ) )
        
        # Instantiate a "SFTP" connection object, with the input remote host, port, username and password.
        connection = sftp_connection( args.host, args.user, args.password, args.port )
        
        # List the files that reside under the input remote directory.
        remote_files = list_remote_directory( args.source )
        
        # No files found under the given remote directory.
        if len( remote_files ) == 0 :
            # Log a message with level CRITICAL on the "root" logger.
            log.critical( "No remote files found" )
            # Close the connection and clean up.
            connection.close()
            # Exit from Python immediately with the given integer exit status (successful termination).
            sys.exit( 0 )
        
        # Files found under the given remote directory.
        # Log a message with level INFO on the "root" logger - print number of files found.
        log.info( "Found %d remote files" % len( remote_files ) )
        
        # Log a message with level INFO on the "root" logger - print the names of the files found.
        ctr = 0
        for file in remote_files:
            ctr = ctr + 1        
            log.info( "File # %2.d : '%s'" % ( ctr, file ) )

        # If the input local destination directory does not already exist then create a directory with the given name 
        # and numeric mode, and log a message with level INFO on the "root" logger.
        if not os.path.exists( args.destination ):
            log.warning( "Folder '%s' does not exist, creating" % args.destination )
            os.mkdir( args.destination, 0o755 )

        # Copy all files from the input remote source directory to the input local destination directory, 
        # preserving their modification time, and log a message with level INFO on the "root" logger.
        log.info( "Downloading remote files" )
        copy_remote_directory( args.source, args.destination )
        log.info( "Downloading remote files completed" )
    except Exception as e:
        # Log a message with level ERROR on the "root" logger - print the exception message.
        log.error( str( e ) )
        # Return a tuple of three values that give information about the exception that is currently being handled, i.e.
        # the type of the exception being handled, the exception instance, and the "Traceback" object, which encapsulates 
        # the call stack at the point where the exception originally occurred.
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # From the returned "Traceback" object, and the execution frame of the current level, and the code object being 
        # executed in this frame, get the filename from which the code was compiled.
        fname = os.path.split( exc_tb.tb_frame.f_code.co_filename )[ 1 ]
        # Log a message with level ERROR on the "root" logger - print the type of the exception being handled, 
        # the filename from which the code was compiled, and the line number where the exception occurred.
        log.error( ( "%s - %s - %s" ) % ( exc_type, fname, exc_tb.tb_lineno ) )
        # Exit from Python immediately with the given integer exit status (abnormal termination).
        sys.exit( 1 )
    else:
        # If no errors were raised,
        # If user also wishes to delete the remote files, delete each file,
        # and log a message with level INFO on the "root" logger.
        if args.delete:
            for file in remote_files:
                delete_remote_file( file )
                log.info( "Deleting remote file '%s' " % file )
        else:            
            log.info( "No remote files deleted" )
            
        # Close the connection and clean up.
        connection.close()

        # Exit from Python immediately with the given integer exit status (successful termination).
        sys.exit( 0 )        
        
# --------------------------------------------------------------------------------------------------
