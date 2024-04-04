
class MainWindow
{
private:
	static LRESULT CALLBACK WndProcCallback(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
protected:
	HWND m_hwnd;
	virtual LRESULT WndProc(UINT message, WPARAM wParam, LPARAM lParam);
	virtual LRESULT DefWndProc(UINT message, WPARAM wParam, LPARAM lParam);
	INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam);
public:
	MainWindow(HINSTANCE hInst);
	virtual ~MainWindow();
	HWND GetHwnd();
	HWND InitInstance(HINSTANCE hInstance, int nCmdShow);
	bool ShowDialog();
};