/**
 * Starry Universe Gravity Engine v2.1.2
 * Update record on 2021-04-21:
 * - Add the document
 * - X/Y Offset(offset[0/1]) added when creating pens, this will increase performance
 *
 * Open file SUGE.cfg2 as configure. Structure:
 * - num: Numbers of stars
 * - X position(a list with num elements)
 * - Y position(a list with num elements)
 * - X velocity(a list with num elements)
 * - Y velocity(a list with num elements)
 * - Gravity(a list with num elements)
 * - Foreground color of the line(a list with num elements, given as BBGGRR in hexdecimal)
 * - Background color
 * - Simulate accuracy
 * - Display frequent(steps per display cicle)
 * - Width of the line(per pixel)
 * - X/Y offset(per pixel)
 */

#include <stdio.h>
#include <math.h>
#include <windows.h>
int num, display_freq, width, offset[2], count, i, j;
COLORREF background_color, *color_ptr;
double simulate_acc, distance, p, q, r;
DWORD WINAPI threadProc(LPVOID lpParamter) {
	FILE *file = fopen("SUGE.cfg2", "r");
	HWND hwnd = (HWND)lpParamter;
	fscanf(file, "%d", &num);
	HDC hdc[num];
	HPEN hpen[num];
	double position[num][2], velocity[num][2], gravity[num];
	COLORREF color[num];
	color_ptr = color;
	for(i=0; i<num; ++i) fscanf(file, "%lf", &position[i][0]);
	for(i=0; i<num; ++i) fscanf(file, "%lf", &position[i][1]);
	for(i=0; i<num; ++i) fscanf(file, "%lf", &velocity[i][0]);
	for(i=0; i<num; ++i) fscanf(file, "%lf", &velocity[i][1]);
	for(i=0; i<num; ++i) fscanf(file, "%lf", &gravity[i]);
	for(i=0; i<num; ++i) fscanf(file, "%lx", &color[i]);
	fscanf(file, "%lx %lf %d %d %d %d", &background_color, &simulate_acc, &display_freq, &width, &offset[0], &offset[1]);
	fclose(file);
	for(i=0; i<num; ++i) {
		hdc[i] = GetDC(hwnd);
		hpen[i] = CreatePen(PS_SOLID, width, color[i]);
		SelectObject(hdc[i], hpen[i]);
		position[i][0] += offset[0];
		position[i][1] += offset[1];
		MoveToEx(hdc[i], position[i][0], position[i][1], 0);
	}
	while(1) {
		for(i=0; i<num; ++i) {
			for(j=0; j<num; ++j) {
				if(i != j) {
					p = position[j][0] - position[i][0];
					q = position[j][1] - position[i][1];
					distance = pow(p * p + q * q, -1.5);
					r = gravity[j] * distance * simulate_acc;
					velocity[i][0] += p * r;
					velocity[i][1] += q * r;
				}
			}
		}
		if(count % display_freq == 0) {
			for(i=0; i<num; ++i) {
				LineTo(hdc[i], position[i][0], position[i][1]);
			}
		}
		for(i=0; i<num; ++i) {
			position[i][0] += velocity[i][0] * simulate_acc;
			position[i][1] += velocity[i][1] * simulate_acc;
		}
		++count;
	}
}
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE prevInstance, LPSTR pCmdLine, int nCmdShow) {
	const char *CLASS_NAME = "SUGEWND";
	WNDCLASS wc = {};
	wc.lpfnWndProc = WindowProc;
	wc.hInstance = hInstance;
	wc.lpszClassName = CLASS_NAME;
	RegisterClass(&wc);
	HWND hwnd = CreateWindowEx(0, CLASS_NAME, "SUGE", 
	WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 
	CW_USEDEFAULT, NULL, NULL, hInstance, NULL);
	if(hwnd == NULL) return 0;
	ShowWindow(hwnd, SW_SHOWMAXIMIZED);
	MSG msg={};
	while(GetMessage(&msg, NULL, 0, 0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return 0;
}
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	switch(uMsg) {
		case WM_DESTROY: {
			PostQuitMessage(0);
			return 0;
		}
		case WM_PAINT: {
			PAINTSTRUCT ps;
			HDC hdc2 = BeginPaint(hwnd, &ps);
			FillRect(hdc2, &ps.rcPaint, CreateSolidBrush(background_color));
			EndPaint(hwnd, &ps);
			return 0;
		}
		case WM_CREATE: {
			HANDLE hThread = CreateThread(NULL, 0, threadProc, (LPVOID)hwnd, 0, NULL);
	    	CloseHandle(hThread);
			return 0;
		}
	}
	return DefWindowProc(hwnd, uMsg, wParam, lParam);
}
