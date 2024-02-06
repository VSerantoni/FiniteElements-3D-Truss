from resources.fea_3D_truss import FeaTruss3D

if __name__ == '__main__':
    path = './test_crane/'
    
    # ===== GEOMETRY =====
    nodesCoor_path = path+'nodesCoor.txt'                   # nodes coordonates
    elementsConnect_path = path+'elementsConnect.txt'       # connectivity of each element
    
    # init FEA
    fea = FeaTruss3D(nodesCoor_path, elementsConnect_path, show=True)

    # ===== BOUNDARY CONDITIONS =====
    restrictedDof_path = path+'restrictedDof.txt'           # bool list of all restricted path
    allLoads_path = path+'loads.txt'                        # list of projected loads path
    
    fea.set_BC(restrictedDof_path, allLoads_path, show_BC=True)
    
    # ===== STIFFNESS =====
    # paremeters
    E = 210e9
    crossSection_path = path+'crossSectionArea.txt'         # cross section area of each element
    
    fea.eval_stiffness(E, crossSection_path)
    
    # ===== SOLVE =====
    fea.solve()
    
    # ===== POST-PROCESSING =====
    fea.eval_reactions()
    fea.eval_stress()
    fea.show_deformed(compare_init=True, colored_stress=True)
    
    