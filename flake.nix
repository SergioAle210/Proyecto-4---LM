{
	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
	};
	outputs = {nixpkgs, ...}: 
	let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      allPkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
		devShells = forAllSystems(system: 
		let
			pkgs = allPkgs.${system};
		in {
		default = pkgs.mkShell {
			packages = [(pkgs.python3.withPackages(pyPkgs: [pyPkgs.colorama pyPkgs.numpy pyPkgs.scikit-fuzzy pyPkgs.matplotlib]))];
		};
		});
		};
}
