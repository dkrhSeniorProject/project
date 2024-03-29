/**
*
* @file infoMessage.c
*
* @brief message containing information about this device
* 
* Info Message Cluster = 0x0007
*
* $Rev: 598 $
* $Author: dsmith $
* $Date: 2010-06-14 16:08:43 -0700 (Mon, 14 Jun 2010) $
*
* YOU ACKNOWLEDGE AND AGREE THAT THE SOFTWARE AND DOCUMENTATION ARE PROVIDED �AS IS� WITHOUT WARRANTY 
* OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, 
* TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL TEXAS INSTRUMENTS 
* OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, 
* BREACH OF WARRANTY, OR OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
* INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR CONSEQUENTIAL DAMAGES, 
* LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY 
* CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
*/
#include "infoMessage.h"
#include "../../Common/printf.h"
#include "../../Common/utilities.h"

/** Display the contents of the infoMessage to console 
@param im the Info Message to display
*/
void printInfoMessage(struct infoMessage* im)
{
    printf("Info ");
    printHeader(im->header);
    printf(", Device Type/subType=%02X/%02X, cause=%02X, numParameters=%u: ", 
           im->deviceType, im->deviceSubType, im->cause, im->numParameters);
    /******************* killing this ......
    for (int i=0; i<im->numParameters; i++)
        printf("[%04X] ", im->parameters[i]);
      **************************************/
    printf("\r\n");
}

/** Outputs the info message as a stream of bytes to memory pointed to by destinationPtr 
Number of bytes streamed is equal to getSizeOfInfoMessage() 
@param im the infoMessage to serialize
@param destination points to a region of memory at least getSizeOfInfoMessage() bytes in size
*/
void serializeInfoMessage(struct infoMessage* im, unsigned char* destinationPtr)
{  
  serializeHeader(im->header, destinationPtr);
  destinationPtr += getSizeOfHeader(im->header);
  *destinationPtr++ = im->deviceType;
  *destinationPtr++ = im->deviceSubType;
  *destinationPtr++ = im->cause;
  *destinationPtr++ = im->numParameters;
  for (int i=0; i < im->numParameters; i++)  //for each Parameter:
  {
    *destinationPtr++ = im->parameters[i] & 0xFF;  //LSB first
    *destinationPtr++ = im->parameters[i] >> 8; 
  }
}

void serializeRouterForwardMessage(struct routerForwardMessage *rfm, unsigned char * destptr)
{
  serializeHeader(rfm->header,destptr);
  destptr += getSizeOfHeader(rfm->header); //offset
  *destptr++ = rfm->lqi;     //lqi
  serializeInfoMessage(rfm->infoMessage,destptr);   
//  destptr += getSizeOfInfoMessage(rfm->infoMessage);  //unnecessaryoffset
}

/** Creates an infoMessage from the stream of bytes starting at source
@param source the beginning of the serialized Info Message
@return an infoMessage from the parsed data
@todo Check that numParameters < MAX_PARAMETERS_IN_INFO_MESSAGE
@todo Point source to length field, and verify if length field == (sourcePtr - source)?
*/
struct infoMessage deserializeInfoMessage(unsigned char* source)
{
    unsigned char* sourcePtr = source;    
    struct infoMessage im;
    struct header hdr = deserializeHeader(sourcePtr);
    im.header = &hdr;
    sourcePtr += getSizeOfHeader(&hdr);
    im.deviceType = *sourcePtr++;
    im.deviceSubType = *sourcePtr++;
    im.cause = *sourcePtr++;
    im.numParameters = *sourcePtr++;
    for (int i=0; i<im.numParameters; i++)  //for each Parameter:
    {
        im.parameters[i] = CONVERT_TO_INT( (*sourcePtr), (*(sourcePtr+1)) );
        sourcePtr += 2;
    }
    return im;
}

/** @return the size of the Info Message, including all KVPs */
unsigned int getSizeOfInfoMessage(struct infoMessage* im)  
{ 
  return getSizeOfHeader(im->header) + 4 + ((im->numParameters)*2);  
}

unsigned int getSizeOfRFM(struct routerForwardMessage *rfm)
{
  return getSizeOfHeader(rfm->header) + sizeof(rfm->lqi) + getSizeOfInfoMessage(rfm->infoMessage);
}

struct routerForwardMessage deserializeRouterForwardMessage(unsigned char* source)
{
  unsigned char* sourcePtr = source;
  struct routerForwardMessage rfm;
  struct infoMessage im;
  struct header hdr = deserializeHeader(sourcePtr);
  rfm.header = &hdr;    //decode
  sourcePtr += getSizeOfHeader(&hdr) ; //shouldn't have to +3 ... i'm worried
  //get size get lqi value
  rfm.lqi = *sourcePtr++;     //hmmmm
  //info message deserialize 
  struct header ihdr = deserializeHeader(sourcePtr);
  im.header = &ihdr;
  sourcePtr += getSizeOfHeader(&ihdr);
  im.deviceType = *sourcePtr++;
  im.deviceSubType = *sourcePtr++;
  im.cause = *sourcePtr++;
  im.numParameters = *sourcePtr++;
  for (int i=0; i<im.numParameters; i++)  //for each Parameter:
  {
      im.parameters[i] = CONVERT_TO_INT( (*sourcePtr), (*(sourcePtr+1)) );
      sourcePtr += 2;
  }

  rfm.infoMessage = &im;  //get end device info message

  return rfm;
}
