#include <stdio.h>
#include <math.h>
#include <windows.h>
#define num 4
#define width 1
#define offsetX 683
#define offsetY 384
double position[num][2] = {{50, 50}, {-50, 0}, {50, -100}, {50, 300}};
double velocity[num][2] = {{-5, 2.5}, {5, -2.5}, {0, 2.5}, {10, -2.5}};
double gravity[num] = {10000, 10000, 10000, 0};
COLORREF color[num] = {0xffffff, 0x00ffff, 0x0000ff, 0xffff00};
COLORREF background_color = 0x000000;
double simulate_acc = 0.00001;
int display_freq = 1000;
double distance;
int count, i, j;
HDC hdc[num];
HPEN hpen[num];
inline double sqr(double x) {return x * x;}
DWORD WINAPI threadProc(LPVOID lpParamter) {
	while(1) {
		for(i=0; i<num; ++i) {
			for(j=0; j<num; ++j) {
				if(i != j) {
					distance = pow(sqr(position[j][0] - position[i][0]) + sqr(position[j][1] - position[i][1]), -1.5);
					velocity[i][0] += ((position[j][0] - position[i][0])) * gravity[j] * distance * simulate_acc;
					velocity[i][1] += ((position[j][1] - position[i][1])) * gravity[j] * distance * simulate_acc;
				}
			}
		}
		if(count % display_freq == 0) {
			for(i=0; i<num; ++i) {
				LineTo(hdc[i], position[i][0] + offsetX, position[i][1] + offsetY);
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
	void *pHWND = &hInstance;
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
			HDC hdc2=BeginPaint(hwnd, &ps);
			FillRect(hdc2, &ps.rcPaint, CreateSolidBrush(background_color));
			EndPaint(hwnd, &ps);
			return 0;
		}
		case WM_CREATE: {
			for(i=0; i<num; ++i) {
				hdc[i] = GetDC(hwnd);
				hpen[i] = CreatePen(PS_SOLID, width, color[i]);
				SelectObject(hdc[i], hpen[i]);
				MoveToEx(hdc[i], position[i][0] + offsetX, position[i][1] + offsetY, 0);
			}
			HANDLE hThread = CreateThread(NULL, 0, threadProc, NULL, 0, NULL);
	    	CloseHandle(hThread);
			return 0;
		}
	}
	return DefWindowProc(hwnd, uMsg, wParam, lParam);
}
