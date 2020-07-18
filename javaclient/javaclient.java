import java.net.Socket;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.util.List;
import java.io.BufferedReader;
import java.io.InputStreamReader;
class javaclient{

	public static final int PORT = 1234;

	public static void main(String[] args) {

		Socket connResult = connectExistingHosts();
		if (connResult != null) {
			connHandling(connResult);
		}
		else
		{
			connResult = connectNewHost();
			if (connResult != null) {
				connHandling(connResult);
			}
		}
		try
		{
			connResult.close();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}	
	private static Socket connectExistingHosts() {
		try {
			Path hostnamePath =Paths.get("hostnames.txt");
			if(Files.exists(hostnamePath)) {
				List<String> hostnames = Files.readAllLines(hostnamePath);
				for (String hostname : hostnames) {
					Socket connResult = connectToHost(hostname);
					if (connResult != null) {
						return connResult;
					}
				}
			}
		}
		catch(Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	private static Socket connectNewHost() {
		return null;
	}
	private static Socket connectToHost(String hostname) {
		System.out.println(String.format("Connecting to %s",hostname));
		try {
			Socket sock = new Socket(hostname, PORT);
			return sock;
		}
		catch (Exception e) {
		}
		return null;
	}
	private static void connHandling(Socket sock) {
		System.out.println("Connected");
		try{
            BufferedReader sockInput =
                new BufferedReader(
                    new InputStreamReader(sock.getInputStream()));
			// DataInputStream sockInput = new DataInputStream(sock.getInputStream());
			DataOutputStream sockOutput = new DataOutputStream(sock.getOutputStream());			

			BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
			String request, response;

			while (true) {
				System.out.print("<<<");
				request = stdin.readLine();
				sockOutput.writeUTF(request);
				sockOutput.flush();
				response = sockInput.readLine();
				System.out.println(response);
			}
		}
		catch (Exception e)
		{
			return;
		}
		// // 
		// while True:
		// 	request = input("<<<")
		// 	sock.sendall(request.encode())
		// 	response = sock.recv(1024).decode()
		// 	print(response)
		// sock.close()
	}
}