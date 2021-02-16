/**November 15 2020
 * Senior Design Team 08
 * University of Akron
 * This program is used to update a 7-Segment display in response
 * to cars entering a leaving the entrance of a parking deck. For demonstration,
 * inputs S3 and S4 on an explorer 16/32 board represent cars entering
 * and leaving respectively.
 */
#include "mcc_generated_files/system.h" // MCC generated code
#include <stdbool.h> // Initialized boolean library

bool _exceedsDisplay = false; // Variable to control plus sign on display

void ms_delay(int N) {
    
    T1CON = 0x8030; // Timer 1 On, prescale 1:256, Tcy as clock
    TMR1 = 0; // Reset TMR1 to zero
    while (TMR1 < N * 62.5) {
    }
}

void us_delay(int N) {
    T1CON = 0x8010; // Timer 1 On, prescale 1:8, 16MHz. Fcy thus 2MHz Clk
    TMR1 = 0; // Reset TMR1 to zero
    while (TMR1 < 2 * N) // Since 2 MHz. Clk, 2 per 1 us
    {
    }
}

void SPI1Init(void) {
    SPI1CON1 = 0x0120; // Master Mode, 8-bit bytes, Idle state low, Active Hi
    // Data changes on clock transition from Active to Idle
    // SCL1 at 16000000/(8*64) = 31.25 kHz.
    SPI1STAT = 0x8000; // enable SPI peripheral
}// SPI1Init
// Send one byte of data and receive one back at the same time

unsigned char writeSPI1(unsigned char j) {
    while (SPI1STATbits.SPITBF); // If SPI1TBF full, just wait. This may not
    // be necessary, but good practice.
    SPI1BUF = j; // Write byte to SPI1BUF
    while (!SPI1STATbits.SPIRBF); // Wait if Receive Not Complete
    return SPI1BUF; // Read the received value
}// writeSPI1

int getDisplayCode(int num)
{
    int displayCode = 0;
    
    switch(num)
    {
        case 0:
            displayCode = 63;
            break;
        case 1:
            displayCode = 6;
            break;
        case 2:
            displayCode = 91;
            break;
        case 3:
            displayCode = 79;
            break;
        case 4:
            displayCode = 102;
            break;
        case 5:
            displayCode = 109;
            break;
        case 6:
            displayCode = 125;
            break;
        case 7:
            displayCode = 7;
            break;
        case 8:
            displayCode = 127;
            break;
        case 9:
            displayCode = 111;
            break;
        default:
            displayCode = 0;
            break;
    }
    
    if(_exceedsDisplay)
    {
        displayCode = displayCode + 128;
    }
    
    return displayCode;
}

void updateDisplay(int num) {
    PORTA = 0x1; // SS back High to enable 7 seg
    writeSPI1(0x00); // Clear display, command found on Sparkfun website 
    writeSPI1(0x00);
    
    if(num > 99)
    {
        num = 99;
        _exceedsDisplay = true;
    }
    
    int lsd = getDisplayCode(num % 10); // Least significant digit
        num = num / 10; 
    int ssd = getDisplayCode(num % 10); // Second least significant digit
        //num = num / 10;
    //int tsd = num % 10; // Third least significant digit
        //num = num / 10;
    //int msd = num % 10; // Most significant digit
        //num = num / 10;
    
        //us_delay(500);  
        //writeSPI1(msd); // Prints the modulated integer from
        //us_delay(500);  // most significant digit to least significant
        //writeSPI1(tsd);
        
        us_delay(500); 
        writeSPI1(lsd);
        us_delay(500); 
        writeSPI1(ssd);
        
        _exceedsDisplay = false;
        
    PORTA = 0x0; // RA0 is SS, assert Low to deselect 7-Seg.
}

void main(void) {
    int showCarsi = 101; // Sets maximum parking capacity
    int showCars = showCarsi; // Parking capacity that will be displayed
    int carCount = showCarsi; // Variable to control showCars
    
    // initialize the device
    SYSTEM_Initialize(); // MCC generated code
    TRISA = 0x0; // PORTA as output
    SPI1Init(); // Initialize SPI Port
    
    writeSPI1(0x00);
    writeSPI1(0x00);
    updateDisplay(showCarsi); // Immediately updates display before given input
    
    while (1) {
        if (PORTDbits.RD13 == 0)
            carCount++; // if S4 pressed increment display counter
        else if (PORTDbits.RD6 == 0)
            carCount--; // else if S3 pressed decrement display counter
        if (carCount != showCars) { // compares carCount to current 
            if(carCount >= 0 && carCount <= showCarsi){ // prevents display from overflowing
            showCars = carCount; //updates showCars to match carCount
            updateDisplay(showCars); //update display
            }
        }
        ms_delay(300); //for testing purposes, slows down button presses
    }
    return 1;
}