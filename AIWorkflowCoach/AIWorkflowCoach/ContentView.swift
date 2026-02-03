import SwiftUI

struct Shortcut: Identifiable {
    let id = UUID()
    var name: String
    var isStarred: Bool = false
}

struct ContentView: View {
    @State private var shortcuts = [Shortcut(name: "Shift + Cmd + L"), Shortcut(name: "Option + Space")]
    @State private var selectedShortcutID: UUID?
    
    // Model State
    @State private var models = ["Llama 3"]
    @State private var currentModel = "Llama 3"
    @State private var showingNewModelAlert = false
    @State private var newModelName = ""
    
    var body: some View {
        VStack(spacing: 0) {
            // 1. Model Selection & Context Reset
            VStack(spacing: 8) {
                HStack {
                    // This creates the Menu you described
                    Menu {
                        ForEach(models, id: \.self) { model in
                            Button(model) { currentModel = model }
                        }
                        
                        Divider()
                        
                        Button("New Model...") {
                            showingNewModelAlert = true
                        }
                    } label: {
                        Label(currentModel, systemImage: "cpu")
                            .font(.headline)
                    }
                    .menuStyle(.borderlessButton)
                    .fixedSize()
                    
                    Spacer()
                }

                Button(action: resetContext) {
                    Label("Reset Context", systemImage: "trash")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
                .tint(.secondary)
            }
            .padding()

            Divider().opacity(0.2)

            // 2. Shortcut List
            List(shortcuts, selection: $selectedShortcutID) { item in
                HStack {
                    Text(item.name).font(.system(.body, design: .monospaced))
                    Spacer()
                    if item.isStarred { Image(systemName: "star.fill").foregroundColor(.yellow) }
                }
                .listRowBackground(Color.clear)
            }
            .listStyle(.plain)
            .frame(minHeight: 180)

            Text("⌘W to Delete • ⌘S to Star")
                .font(.caption2).opacity(0.5).padding(.bottom, 8)
        }
        .frame(width: 250)
        .background(.ultraThinMaterial)
        // 3. The "New Model" Popup
        .alert("Add New Model", isPresented: $showingNewModelAlert) {
            TextField("Model Name (e.g. Mistral)", text: $newModelName)
            Button("Add") {
                if !newModelName.isEmpty {
                    models.append(newModelName)
                    currentModel = newModelName
                    newModelName = ""
                }
            }
            Button("Cancel", role: .cancel) { newModelName = "" }
        } message: {
            Text("Enter the name of the local LLM model you'd like to use.")
        }
        .onAppear(perform: setupKeyListeners)
    }

    func resetContext() { print("Resetting context for \(currentModel)") }

    func setupKeyListeners() {
        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { event in
            let key = event.charactersIgnoringModifiers?.lowercased()
            if event.modifierFlags.contains(.command) {
                if key == "w" { shortcuts.removeAll { $0.id == selectedShortcutID }; return nil }
                if key == "s" {
                    if let index = shortcuts.firstIndex(where: { $0.id == selectedShortcutID }) {
                        shortcuts[index].isStarred.toggle()
                    }
                    return nil
                }
            }
            return event
        }
    }
}  
