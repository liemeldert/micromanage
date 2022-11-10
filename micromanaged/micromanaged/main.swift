//
//  main.swift
//  micromanaged
//
//  Created by Liem Eldert on 2022/11/09.
//

import Foundation
import Starscream


var request = URLRequest(url: URL(string: "http://localhost:8080")!)
request.timeoutInterval = 5
socket = WebSocket(request: request)
socket.delegate = self
socket.connect()

func didReceive(event: WebSocketEvent, client: WebSocket) {
    switch event {
    case .connected(let headers):
        isConnected = true
        print("websocket is connected: \(headers)")
    case .disconnected(let reason, let code):
        isConnected = false
        print("websocket is disconnected: \(reason) with code: \(code)")
    case .text(let string):
        print("Received text: \(string)")
    case .binary(let data):
        print("Received data: \(data.count)")
    case .ping(_):
        break
    case .pong(_):
        break
    case .viabilityChanged(_):
        break
    case .reconnectSuggested(_):
        break
    case .cancelled:
        isConnected = false
    case .error(let error):
        isConnected = false
        handleError(error)
    }
}
