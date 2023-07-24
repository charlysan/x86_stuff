#include <graphics.h>
#include <conio.h>
 
main()
{
   int gd = DETECT, gm;
   int x;

   //init graphics
   initgraph(&gd, &gm, "C:/TC/BGI");

   for (x=0;x<720;x+=4) {
      line(x,0,x,347);
   }
   line(719,0,719,347);

   getch();
   closegraph();
   return 0;
}
