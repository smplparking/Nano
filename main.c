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

int index = 0;

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

int getDisplayCode(int num) {
    int displayCode = 0;

    switch (num) {
        case 0:
            displayCode = 63;
            //displayCode = 252;
            break;
        case 1:
            displayCode = 6;
            //displayCode = 96;
            break;
        case 2:
            displayCode = 91;
            //displayCode = 218;
            break;
        case 3:
            displayCode = 79;
            //displayCode = 242;
            break;
        case 4:
            displayCode = 102;
            //displayCode = 102;
            break;
        case 5:
            displayCode = 109;
            //displayCode = 182;
            break;
        case 6:
            displayCode = 125;
            //displayCode = 190;
            break;
        case 7:
            displayCode = 7;
            //displayCode = 224;
            break;
        case 8:
            displayCode = 127;
            //displayCode = 254;
            break;
        case 9:
            displayCode = 111;
            //displayCode = 246;
            break;
        default:
            displayCode = 0;
            break;
    }

    if (_exceedsDisplay) {
        displayCode = displayCode + 128;
    }

    return displayCode;
}

void TESTFUNC() {
    PORTA = 0x1; // SS back High to enable 7 seg

    writeSPI1(0x00); // Clear display, command found on Sparkfun website
    us_delay(500);
    writeSPI1(0x00);
    us_delay(500);
    int test;

    switch (index) {
            //case 0:
            //test = 0;
            //displayCode = 252;
            //break;
        case 0:
            test = 1;
            //displayCode = 96;
            break;
        case 1:
            test = 2;
            //displayCode = 218;
            break;
        case 2:
            test = 4;
            //displayCode = 242;
            break;
        case 3:
            test = 8;
            //displayCode = 102;
            break;
        case 4:
            test = 16;
            //displayCode = 182;
            break;
        case 5:
            test = 32;
            //displayCode = 190;
            break;
        case 6:
            test = 64;
            //displayCode = 224;
            break;
        case 7:
            test = 128;
        default:
            test = 0;
            break;
    }

    index++;

    writeSPI1(test);
    us_delay(500);
    writeSPI1(test);
    us_delay(500);

    if (index == 8) {
        index = 0;
    }

    PORTA = 0x0;

    return;
}



// transmit byte serially, MSB first

void watchbits(unsigned char data, bool quick) {
    TRISF = 0;
    TRISA = 0;
    // consider leftmost bit
    // set line high if bit is 1, low if bit is 0
    if (data) // if MSB is high
    {
        PORTFbits.RF8 = 1; //send high
    } else {
        PORTFbits.RF8 = 0; //else send low
    }

    // pulse the clock state to indicate that bit value should be read
    PORTFbits.RF6=0;// clock lo
    ms_delay(1); //fake clock
    PORTFbits.RF6=1; //click hi (shift register active)
    
    if (!quick) {
        ms_delay(1000); //wait half a second
    }


}

void bang(unsigned char c, unsigned char lsd) {
    int i, bit;

    for (i = 0; i < 8; i++) {
        bit = (lsd & 0x80);
        watchbits(bit, true);
        lsd <<= 1;
        //PORTFbits.RF6 = 0;
        us_delay(100);
        //PORTFbits.RF6 = 1;
    }
        for (i = 0; i < 8; i++) {
            bit = (c & 0x80);
            watchbits(bit, true);
            c <<= 1;
            //PORTFbits.RF6 = 0;
            us_delay(100);
            //PORTFbits.RF6 = 1;
        }
    }

    void updateDisplay(int num) {
        //PORTA = 0x1; // SS back High to enable 7 seg
        //writeSPI1(0x00); // Clear display, command found on Sparkfun website 
        //writeSPI1(0x00);

        if (num > 99) {
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
        int i, bit;

        for (i = 0; i < 16; i++) {
            bit = 0;
            watchbits(bit, true);

            PORTFbits.RF6 = 0;
            us_delay(100);
            PORTFbits.RF6 = 1;
        }

        us_delay(500);
        //writeSPI1(lsd);
        bang(ssd, lsd);
        us_delay(500);
        //writeSPI1(ssd);
        //bang(ssd);

        _exceedsDisplay = false;
        
        PORTA = 0; //ss low
        ms_delay(1); //wait
        PORTA = 1; //ss hi, display register active
    // shift byte left so next bit will be leftmost

        //PORTA = 0x0; // RA0 is SS, assert Low to deselect 7-Seg.
    }

    void main(void) {
        int showCarsi = 110; // Sets maximum parking capacity
        int showCars = showCarsi; // Parking capacity that will be displayed
        int carCount = showCarsi; // Variable to control showCars

        updateDisplay(showCars);
        /**
       // initialize the device
       SYSTEM_Initialize(); // MCC generated code
       TRISA = 0x0; // PORTA as output
       //SPI1Init(); // Initialize SPI Port
    
       PORTA = 0x1;
       writeSPI1(0x00);
       ms_delay(300);
       writeSPI1(0x00);
       PORTA = 0x0;
       //updateDisplay(showCarsi); // Immediately updates display before given input
         **/
        while (1) {
            /**
            int i;
        
            for (i = 0; i < 80; i++)
                watchbits(0x00, true);
        
            watchbits(0x07, false); //clear
            PORTFbits.RF6=0;
            ms_delay(1);
            PORTFbits.RF6=1;
            //ms_delay(2000);
            for (i = 0; i < 16; i++)
            {
            
            watchbits(0x00, false); //clear
            PORTFbits.RF6=0;
            ms_delay(1);
            PORTFbits.RF6=1;
            }
            //watchbits(0x00, true); //clear
            //ms_delay(2000);
            //watchbits(0x00, false); //1 bit all the way to end
            //watchbits(0x00, false); //clear
            //ms_delay(2000);
        
            //watchbits(0xAA); //alternate bits
            //ms_delay(1000);
            //watchbits(0xFF); //fill all
            //ms_delay(1000);
             * **/


            if (PORTDbits.RD13 == 0)
                carCount++; // if S4 pressed increment display counter
            else if (PORTDbits.RD6 == 0)
                carCount--; // else if S3 pressed decrement display counter
            if (carCount != showCars) { // compares carCount to current 
                if(carCount >= 0 && carCount <= showCarsi){ // prevents display from overflowing
                showCars = carCount; //updates showCars to match carCount
                updateDisplay(showCars); //update display
                }
                //send_8bit_serial_data(8);
                //TESTFUNC();
            }
            ms_delay(300); //for testing purposes, slows down button presses

        }
        return 1;
    }