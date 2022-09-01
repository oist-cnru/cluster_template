import os
import toml
import argparse
import numpy as np

def main(output_dir):
    config_file = 'example/example_config.toml'    
    config = toml.load(config_file)

    config['dataset_path'] = os.path.join(
        os.path.expanduser('~'), 
        'Code', 'cluster_template', 'example', 'dataset_5x11x2.npy'
    )

    # assuming ${PVRNN_SAVE_DIR} is already set
    # new output dir ( This will resolve to: ${PVRNN_SAVE_DIR} / "results" / save_directory)
    config['training']['save_directory'] = 'train'

    # 4 layers in order: sm, second (bottom), third, forth (top)
    layers = config['network']['layers']    
    
    # changing w to last three layers with random values
    new_w = np.random.uniform(low=0.0001, high=0.5, size=3) 
    for i,l in enumerate(layers[1:]):
        l['w'] = new_w[i]

    output_config_file = os.path.join(output_dir, 'config.toml')
    with open(output_config_file, 'w') as fout:
        toml.dump(config, fout)
    # print(toml.dumps(config))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Output directory')
    args = parser.parse_args()

    main(args.dir)